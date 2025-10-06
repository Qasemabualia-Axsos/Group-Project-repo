from django import forms
from .models import Director

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ["name", "bio", "profile_img"]
