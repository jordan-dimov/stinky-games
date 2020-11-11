from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from friendship.models import Friend

from game1.models import InventoryItem, Player, WantsToTrade
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


@login_required
def sell_back_stinky_view(request, inventory_item_id):
    player = get_player(request)
    inventory_item = get_object_or_404(InventoryItem, id=inventory_item_id, user=player.user)
    sell_price = sell_back_stinky(player, inventory_item)
    messages.success(request, "Sold a stinky for {} coin(s).".format(sell_price))
    return redirect('game1:homepage')


@login_required
def view_player_view(request, username):
    player1 = get_player(request)
    player2 = get_object_or_404(Player, user__username=username)
    context = {
        'player': player1,
        'player2': player2,
    }
    return render(request, "game1/player_details.html", context=context)


@login_required
def trade_item_view(request, inv_id):
    inventory_item = get_object_or_404(InventoryItem, id=inv_id, user=request.user)
    other_wtt = WantsToTrade.objects.exclude(user=request.user).order_by('?').first()
    if not other_wtt:
        wtt, created = WantsToTrade.objects.get_or_create(user=request.user, item=inventory_item.item)
        if created:
            messages.info(request, "Stinky is now open for trading: {}".format(wtt.item))
        else:
            messages.warning(request, "Stinky is ALREADY open for trading: {}".format(wtt.item))
    else:
        inventory_item.user = other_wtt.user
        inventory_item.save()
        their_inv = InventoryItem.objects.get(user=other_wtt.user, item=other_wtt.item)
        their_inv.user = request.user
        their_inv.save()
        messages.success(request, "You traded '{}' for '{}'".format(inventory_item.item, their_inv.item))
    return redirect('game1:homepage')


@login_required
def dont_trade_item_view(request, inv_id):
    inventory_item = get_object_or_404(InventoryItem, id=inv_id, user=request.user)
    wtt = WantsToTrade.objects.filter(user=request.user, item=inventory_item.item).first()
    if wtt:
        wtt.delete()
        messages.info(request, "Stinky is no longer open for trading: {}".format(wtt.item))
    else:
        messages.error(request, "This stinky is gone! {}".format(wtt.item))
    return redirect('game1:homepage')
