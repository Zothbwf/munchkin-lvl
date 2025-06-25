from django.shortcuts import render, redirect
# Create your views here.
from .models import Game, Player
from uuid import uuid4
from .forms import PlayerForm


def index(request):
    return render(request, 'index.html')


def join_game(request, game_hash):
    context = {}
    if request.method == "POST":
        game = Game.objects.get(game_hash=game_hash)
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = Player.objects.create(
                player_name=form.cleaned_data['player_name'], player_game=game)
            player.save()
        return redirect('game:join_game', game_hash=game_hash)
    else:
        game = Game.objects.get(game_hash=game_hash)
        players = game.player_set.all()
        form = PlayerForm()
        context['players'] = players
        context['game_hash'] = game_hash
        context['form'] = form
        return render(request, 'game.html', context=context)


def create_game(request):
    new_game = Game.objects.create()
    new_game.game_hash = str(uuid4())[:6]
    new_game.save()
    return redirect('game:join_game', game_hash=new_game.game_hash)


def delete_player(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.delete()
        except Player.DoesNotExist:
            pass
        except Game.DoesNotExist:
            pass
    return redirect('game:join_game', game_hash=game_hash)


def increase_lvl(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.player_lvl += 1
            if player.player_lvl <= 10:
                player.save()
        except Player.DoesNotExist:
            pass
        except Game.DoesNotExist:
            pass
    return redirect('game:join_game', game_hash=game_hash)


def decrease_lvl(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.player_lvl -= 1
            if player.player_lvl >= 1:
                player.save()
        except Player.DoesNotExist:
            pass
        except Game.DoesNotExist:
            pass
    return redirect('game:join_game', game_hash=game_hash)


def increase_equipment(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.player_equipment += 1
            player.save()
        except Player.DoesNotExist:
            pass
        except Game.DoesNotExist:
            pass
    return redirect('game:join_game', game_hash=game_hash)


def decrease_equipment(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            player.player_equipment -= 1
            player.save()
        except Player.DoesNotExist:
            pass
        except Game.DoesNotExist:
            pass
    return redirect('game:join_game', game_hash=game_hash)
