from django import forms
from .models import Locataire

class LocataireForm(forms.ModelForm):
    class Meta:
        model = Locataire
        fields = '__all__'  # Include all fields

from django import forms
from .models import Voiture

class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = '__all__'
        
        
        from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['voiture', 'locataire', 'date_fin']
