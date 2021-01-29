from django.urls import path, include
from dice.api import views as dv
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register(r"dice", dv.DiceViewSet, basename="dice")



urlpatterns = [
    path("", include(router.urls))
]
