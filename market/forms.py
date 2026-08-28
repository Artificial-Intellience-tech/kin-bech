from django import forms
from .models import SellRequest, SellImage


class SellRequestForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        label="Upload images",
    )

    class Meta:
        model = SellRequest
        fields = ["title", "description", "price", "location", "images"]


class SellImageForm(forms.ModelForm):
    class Meta:
        model = SellImage
        fields = ["image"]