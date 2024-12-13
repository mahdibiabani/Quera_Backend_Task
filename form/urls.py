from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import FormViewSet, ResponseViewSet

# Create the main router
router = DefaultRouter()
router.register(r'forms', FormViewSet)

# Create a nested router for responses under forms
forms_router = NestedDefaultRouter(router, r'forms', lookup='form')
forms_router.register(r'responses', ResponseViewSet, basename='form-responses')

urlpatterns = router.urls + forms_router.urls