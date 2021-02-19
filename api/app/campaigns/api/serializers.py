from rest_framework import serializers
from campaigns.models import Campaign, GameSession


class CampaignSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    campaign_start_date = serializers.SerializerMethodField()
    game_sessions = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B %Y")

    def get_campaign_start_date(self, instance):
        if instance.sessions.count() > 0:
            first_session = instance.sessions.first()
            return first_session.start_time.strftime("%d %B %Y")
        return None

    def get_game_sessions(self, instance):
        return instance.sessions.count()


class GameSessionSerializer(serializers.ModelSerializer):
    """Serializer for GameSession objects"""
    campaign = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GameSession
        fields = "__all__"
        read_only_fields = ["current_session"]
