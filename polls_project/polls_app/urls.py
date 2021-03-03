from rest_framework.routers import DefaultRouter

from .views import UserViewSet, LoginView, PollViewSet, QuestionViewSet, ActivePollView


router = DefaultRouter()
router.register(r'login', LoginView, basename='login')
router.register(r'users', UserViewSet, basename='user')
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'active-polls', ActivePollView, basename='active_polls')
urlpatterns = router.urls