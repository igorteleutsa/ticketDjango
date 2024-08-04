from django.core.management.base import BaseCommand
from users.models import Role, Permission
from tickets.models import Status

class Command(BaseCommand):
    help = 'Create default roles, permissions, and statuses'

    def handle(self, *args, **options):
        self.create_permissions()
        self.create_roles()
        self.create_statuses()

    def create_permissions(self):
        permissions = [
            'view_users', 'edit_users', 'delete_users',
            'view_groups', 'edit_groups', 'delete_groups',
            'view_tickets', 'edit_tickets', 'delete_tickets', 'change_ticket_status'
        ]

        for perm in permissions:
            permission, created = Permission.objects.get_or_create(name=perm)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission "{perm}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Permission "{perm}" already exists'))

    def create_roles(self):
        roles_permissions = {
            'Admin': ['view_users', 'edit_users', 'delete_users',
                      'view_groups', 'edit_groups', 'delete_groups',
                      'view_tickets', 'edit_tickets', 'delete_tickets', 'change_ticket_status'],
            'Manager': ['view_users', 'edit_users', 'view_groups',
                        'edit_groups', 'view_tickets', 'edit_tickets', 'change_ticket_status'],
            'Analyst': ['view_tickets', 'change_ticket_status']
        }

        for role_name, permissions in roles_permissions.items():
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Role "{role_name}" already exists'))

            for perm_name in permissions:
                permission = Permission.objects.get(name=perm_name)
                role.permissions.add(permission)

    def create_statuses(self):
        statuses = ['Pending', 'In Review', 'Closed']

        for status in statuses:
            status, created = Status.objects.get_or_create(name=status)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Status "{status}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Status "{status}" already exists'))
