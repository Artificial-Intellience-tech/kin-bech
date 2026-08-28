from django import forms
from .models import SellRequest, SellImage


class SellRequestForm(forms.ModelForm):
    class Meta:
        model = SellRequest
        fields = ["title", "description", "price", "location"]
        # No "images" field here; we handle multiple files manually in the view.


class SellImageForm(forms.ModelForm):
    class Meta:
        model = SellImage
        fields = ["image"]