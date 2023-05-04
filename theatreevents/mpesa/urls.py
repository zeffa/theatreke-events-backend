from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('mpesa', views.PaymentViewSet, basename='mpesa')
urlpatterns = router.urls
