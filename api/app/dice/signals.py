from django.db.models.signals import post_save
from django.dispatch import receiver

from dice.models import Dice, DiceRoll


@receiver(post_save, sender=DiceRoll)
def update_dice_luck_level(sender, instance, *args, **kwargs):
    if instance:
        die = instance.die
        if die.dice_rolls < 3:
            # need at least 3 rolls to determine luck level
            return instance
        
        # TODO: Update to Real working API call for luck level!
        if die.dice_rolls > 7:
            die.luckiness = 2
            die.save()
        
