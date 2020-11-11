from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


DEFAULT_NEW_PLAYER_COINS = 12
DEFAULT_NEW_ITEM_COST = 2


class Stinky(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField(default=DEFAULT_NEW_ITEM_COST)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "stinky"
        verbose_name_plural = "stinkies"


class InventoryItem(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey(Stinky, on_delete=models.CASCADE)
    bought_for = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.item)

    def is_for_trade(self):
        return self.item.for_trade.first()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=DEFAULT_NEW_PLAYER_COINS)

    def __str__(self):
        return "{}".format(self.user)


class WantsToTrade(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wants_to_trade")
    item = models.ForeignKey(Stinky, on_delete=models.CASCADE, related_name='for_trade')
