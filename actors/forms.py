from django import forms
from .models import Actor

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["name", "bio", "profile_img", "movies"]

    # Custom styling with Bootstrap
    def __init__(self, *args, **kwargs):
        super(ActorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
