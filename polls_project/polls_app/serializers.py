from rest_framework import serializers
from rest_framework.utils import model_meta

from django.contrib.auth.hashers import check_password

from .models import *


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'Password is required to log in.'
            )
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username does not exist.'
            )

        if not check_password(password, user.password):
            raise serializers.ValidationError(
                'Wrong password.'
            )

        return {
            'id': user.id,
            'nickname': user.username,
        }


class CustomForeignKeyField(serializers.PrimaryKeyRelatedField):

    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', None)
        self.serializer = kwargs.pop('serializer', None)
        self.pk_field = kwargs.pop('pk_field', None)
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.queryset

    def to_representation(self, value):
        value = super().to_representation(value)
        model_object = self.model.objects.get(id=value)
        return self.serializer(model_object).data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = ('id', 'text', 'type')



class AnswerSerializer(serializers.ModelSerializer):
    question = CustomForeignKeyField(
        model=QuestionModel,
        serializer=QuestionSerializer,
        queryset=QuestionModel.objects.all()
    )

    class Meta:
        model = AnswerModel
        fields = ('id', 'text', 'question')

    def create(self, validated_data):
        text = validated_data.pop('text', None)
        question_id = validated_data.pop('question_id', None)

        if text is None or question_id is None:
            raise serializers.ValidationError('Both "text" and "question_id" fields are required.' )

        question = QuestionModel.objects.get(id=question_id)
        answer = AnswerModel.objects.create(text=text, question=question)

        return answer


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = PollModel
        fields = ('id', 'name', 'description', 'date_start', 'date_end', 'questions')

    def create(self, validated_data):
        questions = validated_data.pop('questions', None)
        created_questions = []

        for question in questions:
            new_question = QuestionModel.objects.create(**question)
            created_questions.append(new_question)

        poll = PollModel.objects.create(**validated_data)

        for created_question in created_questions:
            poll.questions.add(created_question)

        return poll

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)

        for question_data in questions_data:
            question = QuestionModel.objects.get(id=question_data.get('id'))
            for attr, value in question_data.items():
                setattr(question, attr, value)
                question.save()

        if validated_data:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True)

    #     CustomForeignKeyField(
    #     model=QuestionModel,
    #     serializer=QuestionSerializer,
    #     queryset=QuestionModel.objects.all(),
    #     many=True
    # )
    answers = AnswerSerializer(many=True)

    class Meta:
        model = UserModel
        fields = ('username', 'polls', 'answers')
        read_only_fields = ('polls',)

    def update(self, instance, validated_data):
        answers = validated_data.pop('answers', None)
        created_answers = []
        for answer in answers:
            new_answer = AnswerModel.objects.create(**answer)
            created_answers.append(new_answer)

        for created_answer in created_answers:
            instance.answers.add(created_answer)

        instance.save()

        return instance