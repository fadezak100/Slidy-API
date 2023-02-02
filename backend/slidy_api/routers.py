from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from slides.views import SlideViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('slides', SlideViewSet, basename='slides')

urlpatterns = router.urls