from django.urls import path, include
from campaigns.api import views as cv
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register(r'campaigns', cv.CampaignViewSet, basename="campaign")

campaign_router = routers.NestedSimpleRouter(
    router,
    r"campaigns",
    lookup="campaign",
)
campaign_router.register(
    r"gamesessions",
    cv.GameSessionViewSet,
    basename="campaign-gamesessions"
)
# /campaign/
# /campaign/{pk}/
# /campaign/{campaign_pk}/gamesessions/
# /campaign/{campaign_pk}/gamesessions/{pk}/
urlpatterns = [
    path("", include(router.urls)),
    path("", include(campaign_router.urls))
]
