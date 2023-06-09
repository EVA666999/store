from django import forms

from .models import Basket


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        exclude = ("created_timestamp",)
