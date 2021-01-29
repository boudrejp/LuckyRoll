from django.db import models
from django.conf import settings

class Campaign(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    diceset = models.ManyToManyField("dice.DiceSet", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GameSession(models.Model):
    name = models.CharField(max_length=140)
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_session = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
