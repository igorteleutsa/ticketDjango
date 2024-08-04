from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.decorators import permission_required
from .services import (
    list_tickets,
    get_ticket,
    create_ticket,
    update_ticket,
    delete_ticket,
    update_ticket_status,
    list_comments,
    create_comment,
)
from .forms import TicketForm, TicketStatusForm, CommentForm


class TicketListView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = list_tickets(request.user)
        user_roles = request.user.roles.values_list("name", flat=True)
        return render(
            request,
            "tickets/ticket_list.html",
            {"tickets": tickets, "user_roles": user_roles},
        )


class TicketDetailView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_ticket(ticket_id, request.user)
        comments = list_comments(ticket)
        comment_form = CommentForm()
        user_roles = request.user.roles.values_list("name", flat=True)
        return render(
            request,
            "tickets/ticket_detail.html",
            {
                "ticket": ticket,
                "user_roles": user_roles,
                "comments": comments,
                "comment_form": comment_form,
                "has_permission": ticket.user_has_permission(request.user),
            },
        )

    def post(self, request, ticket_id):
        ticket = get_ticket(ticket_id, request.user)
        comment, form = create_comment(ticket_id, request.POST, request.user)
        user_roles = request.user.roles.values_list("name", flat=True)
        if comment:
            return redirect("ticket_detail", ticket_id=ticket.id)
        comments = list_comments(ticket)
        return render(
            request,
            "tickets/ticket_detail.html",
            {
                "ticket": ticket,
                "user_roles": user_roles,
                "comments": comments,
                "comment_form": form,
            },
        )


@method_decorator(permission_required("edit_tickets"), name="dispatch")
class TicketCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TicketForm()
        return render(request, "tickets/ticket_form.html", {"form": form})

    def post(self, request):
        ticket, form = create_ticket(request.POST)
        if ticket:
            return redirect("ticket_list")
        return render(request, "tickets/ticket_form.html", {"form": form})


@method_decorator(permission_required("edit_tickets"), name="dispatch")
class TicketEditView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_ticket(ticket_id, request.user)
        form = TicketForm(instance=ticket)
        return render(request, "tickets/ticket_form.html", {"form": form})

    def post(self, request, ticket_id):
        ticket, form = update_ticket(ticket_id, request.POST, request.user)
        if ticket:
            return redirect("ticket_detail", ticket_id=ticket.id)
        return render(request, "tickets/ticket_form.html", {"form": form})


@method_decorator(permission_required("change_ticket_status"), name="dispatch")
class TicketUpdateStatusView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_ticket(ticket_id, request.user)
        form = TicketStatusForm(instance=ticket)
        return render(request, "tickets/ticket_status_form.html", {"form": form})

    def post(self, request, ticket_id):
        ticket, form = update_ticket_status(ticket_id, request.POST, request.user)
        if ticket:
            return redirect("ticket_detail", ticket_id=ticket.id)
        return render(request, "tickets/ticket_status_form.html", {"form": form})


@method_decorator(permission_required("delete_tickets"), name="dispatch")
class TicketDeleteView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        delete_ticket(ticket_id)
        return redirect("ticket_list")
