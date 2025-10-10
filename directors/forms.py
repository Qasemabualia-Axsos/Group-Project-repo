from django import forms
from .models import Director

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ["name", "bio", "profile_img",]  # now these can be shawn

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
