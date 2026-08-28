from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    """
    Registration form:
    - Accepts usernames in any language (Nepali, Hindi, etc.)
      because the model's username field uses UnicodeUsernameValidator.
    - Accepts any characters in password.
    """
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """
    Profile edit form:
    - Username can be in any language (as allowed by the model).
    - All other fields are normal text/image fields.
    """
    class Meta:
        model = User
        fields = ["username", "email", "bio", "location", "profile_picture"]