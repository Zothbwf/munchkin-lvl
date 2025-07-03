from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import PlayerForm
from .models import Game, Player


@receiver(post_save, sender=Game)
def game_receiver(sender, instance, created, **kwargs):
    game_hash = str(instance.game_hash)
    if not game_hash:
        return
    async_to_sync(get_channel_layer().group_send)(game_hash, {"type": "game.update"})


@receiver(post_delete, sender=Game)
def game_receiver(sender, instance, **kwargs):
    game_hash = str(instance.game_hash)
    if not game_hash:
        return
    async_to_sync(get_channel_layer().group_send)(game_hash, {"type": "game.delete"})


def index(request):
    return render(request, "index.html")


def join_game(request, game_hash):
    context = {}
    try:
        game = Game.objects.get(game_hash=game_hash)
    except Game.DoesNotExist:
        return redirect("game:index")
    players = game.player_set.all()
    players = players.order_by("creation_time")
    form = PlayerForm()
    context["players"] = players
    context["game_hash"] = game_hash
    context["form"] = form
    return render(request, "game.html", context=context)


def join_game_0(request):
    game_hash = request.GET.get("game_hash")
    return redirect("game:join_game", game_hash=game_hash)


def create_game(request):
    new_game = Game.objects.create()
    new_game.game_hash = str(uuid4())[:6]
    new_game.save()
    return redirect("game:join_game", game_hash=new_game.game_hash)


def delete_player(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.delete()
            game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def increase_lvl(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            if player.player_lvl < 10:
                player.player_lvl += 1
                player.save()
                game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def decrease_lvl(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            if player.player_lvl > 1:
                player.player_lvl -= 1
                player.save()
                game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def increase_equipment(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.player_equipment += 1
            player.save()
            game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def decrease_equipment(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            if player.player_equipment > 0:
                player.player_equipment -= 1
                player.save()
                game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def switch_gender(request, player_id, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            gender = player.player_gender
            if gender == "F":
                player.player_gender = "M"
            elif gender == "M":
                player.player_gender = "F"
            player.save()
            game.save()
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player, "game_hash": game_hash}
        return render(request, "player_card.html", context=context)


def remove_game(request, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            game.delete()
        except Game.DoesNotExist:
            pass
        return redirect("game:index")
    else:
        context = {}
        context["game_hash"] = game_hash
        return redirect("game:index")


def load_players(request, game_hash):
    try:
        game = Game.objects.get(game_hash=game_hash)
    except Game.DoesNotExist:
        return ""
    players = game.player_set.all()
    players = players.order_by("creation_time")
    form = PlayerForm()
    context = {}
    context["players"] = players
    context["game_hash"] = game_hash
    return render(request, "players_table.html", context=context)


def add_player(request, game_hash):
    if request.method == "POST":
        game = Game.objects.get(game_hash=game_hash)
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = Player.objects.create(
                player_name=form.cleaned_data["player_name"],
                player_gender=form.cleaned_data["player_gender"],
                player_game=game,
            )
            player.save()
            game.save()
        return redirect("game:load_players", game_hash=game_hash)
