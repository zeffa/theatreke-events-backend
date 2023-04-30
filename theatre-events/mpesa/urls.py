from rest_framework import routers

from mpesa import views

router = routers.DefaultRouter()
router.register('mpesa', views.PaymentViewSet, basename='mpesa')
urlpatterns = router.urls
