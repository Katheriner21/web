from django import forms
from .models import Transmision

class TransmisionForm(forms.ModelForm):
    class Meta:
        model = Transmision
        fields = ['titulo', 'descripcion']