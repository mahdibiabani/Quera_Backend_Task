from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('forms', views.FormViewSet, basename='form')
router.register('responses', views.ResponseViewSet, basename='response')

urlpatterns = router.urls