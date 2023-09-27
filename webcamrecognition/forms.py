from django import forms

class WebcamSessionForm(forms.Form):
    name = forms.CharField(max_length=255)
