from django import forms
from .models import Ticket, Comment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'status', 'note', 'assigned_user', 'assigned_group']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4}),
        }


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
