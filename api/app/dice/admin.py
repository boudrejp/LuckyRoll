from django.contrib import admin
from dice.models import Dice, DiceRoll, DiceSet
# Register your models here.

admin.site.register(Dice)
admin.site.register(DiceRoll)
admin.site.register(DiceSet)
