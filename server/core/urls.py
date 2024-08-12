from django.urls import path, include
from .views import PromptViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"prompts", PromptViewSet, basename="prompt")

urlpatterns = router.urls
