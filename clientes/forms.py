from django import forms
from .models import Favorito

class FavoritoForm(forms.ModelForm):
    class Meta:
        model = Favorito
        fields = ['cliente', 'producto', 'notificar_oferta']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'notificar_oferta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }