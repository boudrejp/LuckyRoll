from django.urls import path, include
from dice.api import views as dv
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register(r"dice", dv.DiceViewSet, basename="dice")

dice_router = routers.NestedSimpleRouter(
    router,
    r"dice",
    lookup="dice"
)

dice_router.register(
    r"dicerolls",
    dv.DiceRollViewSet,
    basename="dice-dicerolls"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(dice_router.urls))
]
