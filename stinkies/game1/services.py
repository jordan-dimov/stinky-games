from django.db import transaction as db_transaction
from game1.game import pick_random_thing
from game1.models import Stinky, InventoryItem


def get_a_stinky():
    stinky_name = pick_random_thing()
    stinky, created = Stinky.objects.get_or_create(name=stinky_name)
    return stinky


@db_transaction.atomic
def buy_a_stinky(player):
    stinky = get_a_stinky()
    if player.coins >= stinky.price:
        item = InventoryItem.objects.create(
            user=player.user,
            item=stinky,
            bought_for=stinky.price,
        )
        player.coins -= stinky.price
        player.save()
        return item
    return None
