from rest_framework import routers

from .views import AuthViewSet, UsersViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='authentication')
router.register('users', UsersViewSet, basename='users')
urlpatterns = router.urls
