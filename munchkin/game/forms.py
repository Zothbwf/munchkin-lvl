from django import forms


class PlayerForm(forms.Form):
    player_name = forms.CharField(max_length=20, label="Имя игрока")
