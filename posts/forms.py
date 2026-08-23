from django import forms
from .models import Post, CATEGORY_CHOICES

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'category', 'title', 'description', 'price', 'location', 'image']
        widgets = {
            'category': forms.Select(choices=CATEGORY_CHOICES),
            'description': forms.Textarea(attrs={'rows': 4}),
            'post_type': forms.Select(attrs={'id': 'post-type-field'}),  # for JS
            'price': forms.NumberInput(attrs={'id': 'price-field'}),
            'location': forms.TextInput(attrs={'id': 'location-field'}),
            'image': forms.ClearableFileInput(attrs={'id': 'image-field'}),
        }

    # We'll control visibility of these in the template with JS
    price = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'id': 'price-field'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'id': 'image-field'})
    )