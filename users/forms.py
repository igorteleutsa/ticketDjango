from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'roles', 'is_active', 'is_staff']
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
