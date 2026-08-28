from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. Up to 150 characters. "
            "Letters and numbers from any language are allowed, "
            "plus @, ., +, -, and _."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
        max_length=300,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.username