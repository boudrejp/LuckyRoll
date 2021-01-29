from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError
from campaigns.models import GameSession, Campaign

FOUR_SIDED = 4
SIX_SIDED = 6
EIGHT_SIDED = 8
TEN_SIDED = 10
TWELVE_SIDED = 12
TWENTY_SIDED = 20
ONE_HUNDRED_SIDED = 100
SIDES = (
    (FOUR_SIDED, "Four"),
    (SIX_SIDED, "Six"),
    (EIGHT_SIDED, "Eight"),
    (TEN_SIDED, "Ten"),
    (TWELVE_SIDED, "Twelve"),
    (TWENTY_SIDED, "Twenty"),
    (ONE_HUNDRED_SIDED, "OneHundred")
)


class Dice(models.Model):
    LUCK_LEVEL = (
        (0, "cold"),
        (1, "neutral"),
        (2, "hot")
    )
    name = models.CharField(max_length=60)
    sides = models.IntegerField(choices=SIDES)
    luckiness = models.IntegerField(choices=LUCK_LEVEL, default=1)
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class DiceSet(models.Model):
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    four_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': FOUR_SIDED},
        blank=True, null=True,
        related_name="four_sided"
    )
    six_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': SIX_SIDED},
        blank=True, null=True,
        related_name="six_sided"

    )
    eight_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': EIGHT_SIDED},
        blank=True, null=True,
        related_name="eight_sided"

    )
    ten_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': TEN_SIDED},
        blank=True, null=True,
        related_name="ten_sided"

    )
    twelve_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': TWELVE_SIDED},
        blank=True, null=True,
        related_name="twelve_sided"
    )
    twenty_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': TWENTY_SIDED},
        blank=True, null=True,
        related_name="twenty_sided"
    )
    one_hundred_sided = models.ForeignKey(
        Dice,
        on_delete=models.CASCADE,
        limit_choices_to={'sides': ONE_HUNDRED_SIDED},
        blank=True, null=True,
        related_name="one_hundred_sided"
    )


class DiceRoll(models.Model):

    value = models.IntegerField()
    sides = models.IntegerField(choices=SIDES)
    image = models.ImageField()
    die = models.ForeignKey(
        Dice, on_delete=models.CASCADE, related_name="dice_rolls"
    )
    game_session = models.ForeignKey(
        GameSession, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.dice is not None:
            self.sides = self.dice.sides

        return super().save(*args, **kwargs)

    def clean(self):
        if self.sides is not None:
            if self.value < 1 or self.value > self.sides:
                raise ValidationError(
                    f"Value: {self.value} is < 1 or bigger than {self.sides}"
                )

    def __str__(self):
        return f"Sides: {str(self.sides)}, Value: {str(self.value)}"
