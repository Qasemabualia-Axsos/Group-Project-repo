from django import forms
from .models import Actor
from movies.models import Movies

class ActorForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(
        queryset=Movies.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Actor
        fields = ["name", "bio", "profile_img", "movies"]

    def __init__(self, *args, **kwargs):
        super(ActorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
