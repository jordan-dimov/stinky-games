from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from game1.models import Player
from game1.services import buy_a_stinky


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