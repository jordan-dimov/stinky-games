from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from friendship.models import Friend

from game1.models import InventoryItem, Player
from game1.services import buy_a_stinky, sell_back_stinky


def get_player(request):
    if request.user.is_authenticated:
        player, created = Player.objects.get_or_create(user=request.user)
        return player
    return None


@login_required
def homepage_view(request):
    player = get_player(request)

    context = {
        'player': player,
        'inventory': request.user.inventory.all(),
        'friends': Friend.objects.friends(request.user),
    }
    return render(request, "game1/homepage.html", context=context)


@login_required
def buy_new_stinky_view(request):
    player = get_player(request)
    new_item = buy_a_stinky(player)

    if new_item:
        messages.success(request, "Congratulations! You bought a new stinky: {}".format(new_item.item))
    else:
        messages.error(request, "Sorry! You don't have enough coins for a new stinky.")

    return redirect('game1:homepage')


@login_required()
def sell_back_stinky_view(request, inventory_item_id):
    player = get_player(request)
    inventory_item = get_object_or_404(InventoryItem, id=inventory_item_id, user=player.user)
    sell_price = sell_back_stinky(player, inventory_item)
    messages.success(request, "Sold a stinky for {} coin(s).".format(sell_price))
    return redirect('game1:homepage')

