
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from dice.api.serializers import DiceSerializer, DiceRollSerializer
from dice.models import Dice, DiceRoll


class DiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiceSerializer


    def get_queryset(self):
        user = self.request.user
        return Dice.objects.filter(owner=user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class DiceRollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiceRollSerializer

    def get_queryset(self):
        dice_pk = self.kwargs.get("dice_pk")
        filtered_dice_rolls = DiceRoll.objects.filter(
            die=dice_pk
        )
        return filtered_dice_rolls
    
    def perform_create(self, serializer):
        dice_pk = self.kwargs.get("dice_pk")
        die = get_object_or_404(Dice, pk=dice_pk)

        serializer.save(die=die)