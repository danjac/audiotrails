from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

User = get_user_model()


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("send_recommendations_email",)
        help_texts = {
            "send_recommendations_email": "We will send you recommendations for new podcasts every week",
        }
