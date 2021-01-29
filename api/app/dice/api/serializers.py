from django.db.models import Avg
from rest_framework import serializers
from dice.models import Dice, DiceRoll
from campaigns.models import GameSession

class DiceSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    dice_roll_count = serializers.SerializerMethodField()
    avg_roll = serializers.SerializerMethodField()
    luckiness = serializers.CharField(read_only=True, source="get_luckiness_display")
    sides = serializers.IntegerField(read_only=True)
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Dice
        fields = "__all__"

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B %Y")
    
    def get_dice_roll_count(self, instance):
        return instance.dice_rolls.count()
    
    def get_avg_roll(self, instance):
        if instance.dice_rolls.count() < 1:
            return None

        return instance.dice_rolls.aggregate(Avg("value"))

class DiceRollSerializer(serializers.ModelSerializer):
    die = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = DiceRoll
        fields = "__all__"
        read_only_fields = ["sides"]