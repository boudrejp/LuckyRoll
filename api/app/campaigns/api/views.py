from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from campaigns.models import Campaign
from app.permissions import IsAuthor, IsAuthorOrReadOnly
from campaigns.api.serializers import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    serializer_class = CampaignSerializer

    def get_queryset(self):
        user = self.request.user
        return Campaign.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
