from django.urls import path
from . import views

urlpatterns = [
    path("", views.TicketListView.as_view(), name="ticket_list"),
    path(
        "ticket/<int:ticket_id>/",
        views.TicketDetailView.as_view(),
        name="ticket_detail",
    ),
    path("ticket/add/", views.TicketCreateView.as_view(), name="ticket_add"),
    path(
        "ticket/edit/<int:ticket_id>/",
        views.TicketEditView.as_view(),
        name="ticket_edit",
    ),
    path(
        "ticket/update_status/<int:ticket_id>/",
        views.TicketUpdateStatusView.as_view(),
        name="ticket_update_status",
    ),
    path(
        "ticket/delete/<int:ticket_id>/",
        views.TicketDeleteView.as_view(),
        name="ticket_delete",
    ),
]
