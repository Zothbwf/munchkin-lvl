from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_game/", views.create_game, name="create_game"),
    path("join_game/0/", views.join_game_0, name="join_game_0"),
    path("join_game/<game_hash>/", views.join_game, name="join_game"),
    path(
        "join_game/<game_hash>/delete_player/<player_id>",
        views.delete_player,
        name="delete_player",
    ),
    path(
        "join_game/<game_hash>/increase_lvl/<player_id>",
        views.increase_lvl,
        name="increase_lvl",
    ),
    path(
        "join_game/<game_hash>/decrease_lvl/<player_id>",
        views.decrease_lvl,
        name="decrease_lvl",
    ),
    path(
        "join_game/<game_hash>/increase_equipment/<player_id>",
        views.increase_equipment,
        name="increase_equipment",
    ),
    path(
        "join_game/<game_hash>/decrease_equipment/<player_id>",
        views.decrease_equipment,
        name="decrease_equipment",
    ),
    path(
        "join_game/<game_hash>/switch_gender/<player_id>",
        views.switch_gender,
        name="switch_gender",
    ),
    path("remove_game/<game_hash>/", views.remove_game, name="remove_game"),
    path("load_players/<game_hash>/", views.load_players, name="load_players"),
    path("add_player/<game_hash>/", views.add_player, name="add_player"),
]
