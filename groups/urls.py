from django.urls import path
from . import views

urlpatterns = [
    path('', views.GroupListView.as_view(), name='group_list'),
    path('group/<int:group_id>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('group/add/', views.GroupCreateView.as_view(), name='group_add'),
    path('group/edit/<int:group_id>/', views.GroupEditView.as_view(), name='group_edit'),
    path('group/delete/<int:group_id>/', views.GroupDeleteView.as_view(), name='group_delete'),
]
