# directors/forms.py
from django import forms
from .models import Director
from django.core.exceptions import ValidationError

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = [
            "name", "bio", "profile_img",
            "date_of_birth", "nationality", "website", "imdb_url", "is_active"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Example: Christopher Nolan"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "A short biography..."}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "nationality": forms.TextInput(attrs={"placeholder": "British / American / ..."}),
            "website": forms.URLInput(attrs={"placeholder": "https://..."}),
            "imdb_url": forms.URLInput(attrs={"placeholder": "https://www.imdb.com/name/..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 3:
            raise ValidationError("The name must be at least 3 characters long.")
        return name
