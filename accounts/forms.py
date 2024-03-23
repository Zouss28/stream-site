from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Specify only the fields you want to include

    # Override labels, help_texts, and error_messages as needed
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your desired username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'
