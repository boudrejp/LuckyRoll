from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from app.permissions import IsAuthor
from campaigns.models import Campaign
from campaigns.api.serializers import CampaignSerializer, GameSessionSerializer
from campaigns.models import GameSession


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthor, IsAuthenticated]
    serializer_class = CampaignSerializer

    def get_queryset(self):
        user = self.request.user
        return Campaign.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class GameSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSessionSerializer

    def get_queryset(self):
        campaign_pk = self.kwargs.get("campaign_pk")
        filtered_sessions = GameSession.objects.filter(
            campaign=campaign_pk
        )
        return filtered_sessions

    def perform_create(self, serializer):
        campaign_pk = self.kwargs.get("campaign_pk")
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if campaign.sessions.filter(
            name=serializer.validated_data['name']
        ).exists():
            raise ValidationError("You have a Session with this name already.")
        serializer.save(campaign=campaign)
