import datetime

from django.db import models

# Create your models here.


class Game(models.Model):
    game_hash = models.CharField(max_length=6)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game code = {self.game_hash}"


class Player(models.Model):
    GENDER_CHOICES = (
        ("M", "Мужской"),
        ("F", "Женский"),
    )
    player_name = models.CharField(max_length=20)
    player_lvl = models.IntegerField(default=1)
    player_equipment = models.IntegerField(default=0)
    player_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player_hash = models.CharField(max_length=20)
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    player_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")

    class Meta:
        indexes = [models.Index(fields=["player_hash"])]

    def __str__(self):
        return self.player_name

    def power(self):
        return self.player_equipment + self.player_lvl

    def gender(self):
        if self.player_gender == "M":
            return "♂ Мужчина"
        else:
            return "♀ Женщина"
