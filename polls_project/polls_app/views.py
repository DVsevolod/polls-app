from datetime import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth import authenticate, login

from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from .permissions import UserOnly


class LoginView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def list(self, request, *args, **kwargs):
        username = request.GET.get('username', None)
        password = request.GET.get('password', None)
        anon_id = request.GET.get('anon_id', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        elif anon_id is not None:
            try:
                anon_user = UserModel.objects.get(anon_id=anon_id)
            except UserModel.DoesNotExist:
                anon_username = 'AnonymUser' + str(anon_id)
                anon_user = UserModel.objects.create(username=anon_username, anon_id=int(anon_id))
            login(request, anon_user)
            return Response({"status": "ok-anonymous"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes_by_action = {'list': [IsAdminUser],
                                    'default': [UserOnly | IsAdminUser]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = PollModel.objects.all()
    permission_classes = (IsAdminUser,)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()
    permission_classes = (IsAdminUser,)


class ActivePollView(viewsets.ViewSet):
    @swagger_auto_schema(responses={"200": PollSerializer})
    def list(self, request):
        """

        :return:
        список активных опросов
        """
        polls = PollModel.objects.filter(date_end__gte=datetime.now().date())
        serializer = PollSerializer(polls, many=True)
        return Response({"polls": serializer.data})

    @swagger_auto_schema(responses={"200": PollSerializer})
    def retrieve(self, request, pk):
        """

        :return:
        выбранный опрос
        """
        poll = PollModel.objects.get(id=pk)
        serializer = PollSerializer(poll)
        return Response({"poll": serializer.data})

    @swagger_auto_schema(responses={"200": UserSerializer})
    def update(self, request, pk):
        """

        сохранение ответа происходит через update метод конкретного активного опроса.
        ответы и опросы являются полями со связью many2many модели User.

        Request body:

            answers:
                    text: answer text,
                    question: question_id

                    text: answer text,
                    question: question_id

        :return:
        объект модели User с сохраненными ответами и пройденными опросами.
        """
        user_id = request.user.id
        user = get_object_or_404(UserModel.objects.all(), pk=user_id)
        poll = get_object_or_404(PollModel.objects.all(), pk=pk)
        user.polls.add(poll)
        data = request.data

        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response(serializer.data)