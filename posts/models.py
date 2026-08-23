from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


POST_TYPE_CHOICES = [
    ('BUY', 'Buy'),
    ('SELL', 'Sell'),
]


CATEGORY_CHOICES = [
    ('FURNITURE', 'Furniture'),
    ('VEHICLES', 'Vehicles'),
    ('FLATS', 'Flats'),
    ('HOUSES', 'Houses'),
    ('ELECTRONICS', 'Electronics'),
    ('MOBILE_PHONES', 'Mobile Phones'),
    ('COMPUTERS', 'Computers'),
    ('CLOTHING', 'Clothing'),
    ('JOBS', 'Jobs'),
    ('SERVICES', 'Services'),
    ('OTHER', 'Other'),
]


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=5, choices=POST_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_type} - {self.title} by {self.user.username}"

    def clean(self):
        super().clean()
        if self.post_type == 'BUY':
            if self.price:
                raise ValidationError({'price': 'Buy requests should not have a price.'})
            # Optionally also enforce no image for BUY:
            # if self.image:
            #     raise ValidationError({'image': 'Buy requests should not have an image.'})