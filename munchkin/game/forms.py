from django import forms

from .models import Player


class PlayerForm(forms.Form):
    player_name = forms.CharField(max_length=20, label="Имя игрока")
    player_gender = forms.ChoiceField(
        choices=Player.GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "gender-select"}),
        label="Пол",
    )
