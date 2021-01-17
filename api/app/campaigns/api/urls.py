from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaigns.api import views as cv


router = DefaultRouter()
router.register(r"campaigns", cv.CampaignViewSet, basename="Campaign")

urlpatterns = [
    path("", include(router.urls)),
]
