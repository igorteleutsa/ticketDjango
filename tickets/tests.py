from django.test import TestCase
from django.urls import reverse
from users.models import User, Role, Permission
from tickets.models import Ticket, Status
from groups.models import Group
from tickets.forms import TicketForm, TicketStatusForm, CommentForm


class TicketViewTest(TestCase):
    def setUp(self):
        # Set up users, roles, permissions, statuses, groups, and tickets
        self.admin_role = Role.objects.create(name='Admin')
        self.manager_role = Role.objects.create(name='Manager')
        self.analyst_role = Role.objects.create(name='Analyst')

        self.edit_permission = Permission.objects.create(name='edit_tickets')
        self.status_permission = Permission.objects.create(name='change_ticket_status')
        self.comment_permission = Permission.objects.create(name='comment_tickets')
        self.delete_permission = Permission.objects.create(name='delete_tickets')

        self.admin_role.permissions.add(self.edit_permission, self.status_permission, self.comment_permission,
                                        self.delete_permission)
        self.manager_role.permissions.add(self.edit_permission, self.status_permission, self.comment_permission)
        self.analyst_role.permissions.add(self.status_permission, self.comment_permission)

        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123')
        self.admin_user.roles.add(self.admin_role)

        self.manager_user = User.objects.create_user(email='manager@example.com', password='password123')
        self.manager_user.roles.add(self.manager_role)

        self.analyst_user = User.objects.create_user(email='analyst@example.com', password='password123')
        self.analyst_user.roles.add(self.analyst_role)

        self.status = Status.objects.create(name='Open')
        self.group = Group.objects.create(name='Group 1')
        self.group.members.add(self.admin_user, self.manager_user, self.analyst_user)

        self.ticket = Ticket.objects.create(
            name='Test Ticket',
            status=self.status,
            assigned_user=self.admin_user,
            assigned_group=self.group
        )

    def test_ticket_list_view(self):
        self.client.login(email='admin@example.com', password='password123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_list.html')
        self.assertContains(response, self.ticket.name)

    def test_ticket_detail_view(self):
        self.client.login(email='admin@example.com', password='password123')
        response = self.client.get(reverse('ticket_detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_detail.html')
        self.assertContains(response, self.ticket.name)

    def test_ticket_create_view(self):
        self.client.login(email='admin@example.com', password='password123')
        response = self.client.post(reverse('ticket_add'), {'name': 'New Ticket', 'status': self.status.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ticket.objects.filter(name='New Ticket').exists())

    def test_ticket_edit_view(self):
        self.client.login(email='admin@example.com', password='password123')
        response = self.client.post(reverse('ticket_edit', args=[self.ticket.id]),
                                    {'name': 'Updated Ticket', 'status': self.status.id})
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.name, 'Updated Ticket')

    def test_ticket_update_status_view(self):
        self.client.login(email='analyst@example.com', password='password123')
        new_status = Status.objects.create(name='Closed')
        response = self.client.post(reverse('ticket_update_status', args=[self.ticket.id]), {'status': new_status.id})
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, new_status)

    def test_ticket_delete_view(self):
        self.client.login(email='admin@example.com', password='password123')
        response = self.client.post(reverse('ticket_delete', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_comment_create_view(self):
        self.client.login(email='analyst@example.com', password='password123')
        response = self.client.post(reverse('ticket_detail', args=[self.ticket.id]), {'text': 'Test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.ticket.comments.filter(text='Test comment').exists())

    def test_ticket_permissions(self):
        self.client.login(email='analyst@example.com', password='password123')
        # Test creating a ticket (should fail)
        response = self.client.post(reverse('ticket_add'), {'name': 'New Ticket', 'status': self.status.id})
        self.assertEqual(response.status_code, 403)

        # Test editing a ticket (should fail)
        response = self.client.post(reverse('ticket_edit', args=[self.ticket.id]),
                                    {'name': 'Updated Ticket', 'status': self.status.id})
        self.assertEqual(response.status_code, 403)

        # Test updating ticket status (should succeed)
        new_status = Status.objects.create(name='Closed')
        response = self.client.post(reverse('ticket_update_status', args=[self.ticket.id]), {'status': new_status.id})
        self.assertEqual(response.status_code, 302)

        # Test deleting a ticket (should fail)
        response = self.client.post(reverse('ticket_delete', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 403)
