from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
    pass
