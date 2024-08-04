from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .models import User
from .forms import UserForm, UserRegistrationForm


def register_user(form_data):
    form = UserRegistrationForm(form_data)
    if form.is_valid():
        user = form.save()
        return user, None
    return None, form


def get_user(user_id):
    return get_object_or_404(User, id=user_id)


def create_user(form_data):
    form = UserForm(form_data)
    if form.is_valid():
        user = form.save()
        return user, None
    return None, form


def update_user(user_id, form_data):
    user = get_object_or_404(User, id=user_id)
    form = UserForm(form_data, instance=user)
    if form.is_valid():
        user = form.save()
        return user, None
    return None, form


def delete_user(user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()


def list_users():
    return User.objects.all()


def logout_user(request):
    logout(request)
