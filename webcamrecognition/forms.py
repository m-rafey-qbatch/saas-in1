from django import forms
from socialmedia.models import Unit  # Import the Unit model from your models.py

class WebcamSessionForm(forms.Form):
    UNIT_CHOICES = Unit.UNIT_CHOICES  # Use the choices from your Unit model

    name = forms.ChoiceField(choices=UNIT_CHOICES, required=False)  
    other_name = forms.CharField(max_length=255, required=False) 

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        other_name = cleaned_data.get('other_name')

        if not name and not other_name:
            raise forms.ValidationError("You must select a unit or enter 'Other'.")

        return cleaned_data