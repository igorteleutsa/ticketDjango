from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.UserListView.as_view(), name='user_list'),
    path('user/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/add/', views.UserCreateView.as_view(), name='user_add'),
    path('user/edit/<int:user_id>/', views.UserEditView.as_view(), name='user_edit'),
    path('user/delete/<int:user_id>/', views.UserDeleteView.as_view(), name='user_delete'),
]
