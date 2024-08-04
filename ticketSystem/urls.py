from django.contrib import admin
from django.urls import path, include
from ticketSystem.views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("tickets/", include("tickets.urls")),
    path("users/", include("users.urls")),
    path("groups/", include("groups.urls")),
]
