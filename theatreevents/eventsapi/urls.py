from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('clients', views.ClientViewSet, basename='clients')
router.register('events', views.EventViewSet, basename='events')
router.register('venues', views.VenueViewSet, basename='venues')
urlpatterns = router.urls
