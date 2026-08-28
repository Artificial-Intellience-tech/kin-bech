from django import forms
from .models import SellRequest, SellImage


class SellRequestForm(forms.ModelForm):
    class Meta:
        model = SellRequest
        fields = ["title", "description", "price", "location"]
        # Images are handled via raw <input type="file" multiple> in the template.


class SellImageForm(forms.ModelForm):
    class Meta:
        model = SellImage
        fields = ["image"]