from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Game, Player
from uuid import uuid4
from .forms import PlayerForm


def index(request):
    return render(request, 'index.html')


def join_game(request, game_hash):
    context = {}
    try:
        game = Game.objects.get(game_hash=game_hash)
    except Game.DoesNotExist:
        return redirect('game:index')
    players = game.player_set.all()
    players = players.order_by('creation_time')
    form = PlayerForm()
    context['players'] = players
    context['game_hash'] = game_hash
    context['form'] = form
    return render(request, 'game.html', context=context)


def join_game_0(request):
    game_hash = request.GET.get('game_hash')
    return redirect('game:join_game', game_hash=game_hash)


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
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def increase_lvl(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            update_fields = ['player_lvl']
            if player.player_lvl < 10:
                player.player_lvl += 1
                player.save(update_fields=update_fields)
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def decrease_lvl(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            update_fields = ['player_lvl']
            if player.player_lvl > 1:
                player.player_lvl -= 1
                player.save(update_fields=update_fields)
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def increase_equipment(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            update_fields = ['player_equipment']
            player.player_equipment += 1
            player.save(update_fields=update_fields)
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def decrease_equipment(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            update_fields = ['player_equipment']
            if player.player_equipment > 0:
                player.player_equipment -= 1
                player.save(update_fields=update_fields)
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def switch_gender(request, player_id, game_hash):
    if request.method == 'POST':
        try:
            game = Game.objects.get(game_hash=game_hash)
            player = Player.objects.get(id=player_id, player_game=game)
            update_fields = ['player_gender']
            gender = player.player_gender
            if gender == 'F':
                player.player_gender = 'M'
            elif gender == 'M':
                player.player_gender = 'F'
            player.save(update_fields=update_fields)
        except Player.DoesNotExist:
            return ""
        except Game.DoesNotExist:
            return ""
        context = {"player": player,
                   "game_hash": game_hash}
        return render(request, 'player_card.html', context=context)


def remove_game(request, game_hash):
    if request.method == "POST":
        try:
            game = Game.objects.get(game_hash=game_hash)
            game.delete()
        except Game.DoesNotExist:
            pass
        return redirect('game:index')
    else:
        context = {}
        context['game_hash'] = game_hash
        return redirect('game:index')


def load_players(request, game_hash):
    try:
        game = Game.objects.get(game_hash=game_hash)
    except Game.DoesNotExist:
        return ""
    players = game.player_set.all()
    players = players.order_by('creation_time')
    form = PlayerForm()
    context = {}
    context['players'] = players
    context['game_hash'] = game_hash
    return render(request, 'players_table.html', context=context)


def add_player(request, game_hash):
    if request.method == "POST":
        game = Game.objects.get(game_hash=game_hash)
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = Player.objects.create(
                player_name=form.cleaned_data['player_name'], player_gender=form.cleaned_data['player_gender'], player_game=game)
            player.save()
        return redirect('game:load_players', game_hash=game_hash)
