from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from users.decorators import permission_required
from .services import register_user, get_user, create_user, update_user, delete_user, list_users, logout_user
from .forms import UserForm, UserRegistrationForm


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        user, form = register_user(request.POST)
        if user:
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout_user(request)
        return redirect('login')

    def post(self, request):
        logout_user(request)
        return redirect('login')


@method_decorator(permission_required('view_users'), name='dispatch')
class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = list_users()
        return render(request, 'users/user_list.html', {'users': users})


@method_decorator(permission_required('view_users'), name='dispatch')
class UserDetailView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_user(user_id)
        return render(request, 'users/user_detail.html', {'user': user})


@method_decorator(permission_required('edit_users'), name='dispatch')
class UserCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserForm()
        return render(request, 'users/user_form.html', {'form': form})

    def post(self, request):
        user, form = create_user(request.POST)
        if user:
            return redirect('user_list')
        return render(request, 'users/user_form.html', {'form': form})


@method_decorator(permission_required('edit_users'), name='dispatch')
class UserEditView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_user(user_id)
        form = UserForm(instance=user)
        return render(request, 'users/user_form.html', {'form': form})

    def post(self, request, user_id):
        user, form = update_user(user_id, request.POST)
        if user:
            return redirect('user_detail', user_id=user.id)
        return render(request, 'users/user_form.html', {'form': form})


@method_decorator(permission_required('delete_users'), name='dispatch')
class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        delete_user(user_id)
        return redirect('user_list')
