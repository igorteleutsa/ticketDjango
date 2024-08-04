from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Ticket, Comment
from .forms import TicketForm, TicketStatusForm, CommentForm


def list_tickets(user):
    user_roles = user.roles.values_list('name', flat=True)
    if 'Admin' in user_roles:
        return Ticket.objects.all()
    else:
        return Ticket.objects.filter(
            Q(assigned_user=user) |
            Q(assigned_group__members=user)
        ).distinct()


def get_ticket(ticket_id, user):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not ticket.user_has_permission(user):
        raise PermissionDenied
    return ticket


def create_ticket(form_data):
    form = TicketForm(form_data)
    if form.is_valid():
        return form.save(), None
    return None, form


def update_ticket(ticket_id, form_data, user):
    ticket = get_ticket(ticket_id, user)
    form = TicketForm(form_data, instance=ticket)
    if form.is_valid():
        return form.save(), None
    return None, form


def delete_ticket(ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()


def update_ticket_status(ticket_id, form_data, user):
    ticket = get_ticket(ticket_id, user)
    form = TicketStatusForm(form_data, instance=ticket)
    if form.is_valid():
        return form.save(), None
    return None, form


def list_comments(ticket):
    return ticket.comments.all()


def create_comment(ticket_id, form_data, user):
    ticket = get_ticket(ticket_id, user)
    form = CommentForm(form_data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.ticket = ticket
        comment.author = user
        comment.save()
        return comment, None
    return None, form
