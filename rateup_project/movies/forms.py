from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'description',
            'release_date',
            'duration',
            'poster',
            'rating',
            'categories',   
            'actors',       
            'directors'    
        ]
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'actors': forms.CheckboxSelectMultiple(),
            'categories': forms.CheckboxSelectMultiple(),
            'directors': forms.CheckboxSelectMultiple(),
        }
