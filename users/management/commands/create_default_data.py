from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role, Permission
from groups.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default users and groups'

    def handle(self, *args, **options):
        self.create_roles_and_permissions()
        self.create_users()
        self.create_groups()

    def create_roles_and_permissions(self):
        permissions = [
            'view_users', 'edit_users', 'delete_users',
            'view_groups', 'edit_groups', 'delete_groups',
            'view_tickets', 'edit_tickets', 'delete_tickets', 'change_ticket_status'
        ]

        for perm in permissions:
            Permission.objects.get_or_create(name=perm)

        roles_permissions = {
            'Admin': permissions,
            'Manager': ['view_users', 'edit_users', 'view_groups', 'edit_groups', 'view_tickets', 'edit_tickets', 'change_ticket_status'],
            'Analyst': ['view_tickets', 'change_ticket_status']
        }

        for role_name, perm_names in roles_permissions.items():
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created'))
            for perm_name in perm_names:
                permission = Permission.objects.get(name=perm_name)
                role.permissions.add(permission)

    def create_users(self):
        # Create Admin
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={'password': 'password123'}
        )
        if created:
            admin.set_password('password123')
            admin.save()
        admin.roles.set(Role.objects.filter(name='Admin'))

        # Create Managers
        for i in range(1, 4):
            manager, created = User.objects.get_or_create(
                email=f'manager{i}@example.com',
                defaults={'password': 'password123'}
            )
            if created:
                manager.set_password('password123')
                manager.save()
            manager.roles.set(Role.objects.filter(name='Manager'))

        # Create Analysts
        for i in range(1, 4):
            analyst, created = User.objects.get_or_create(
                email=f'analyst{i}@example.com',
                defaults={'password': 'password123'}
            )
            if created:
                analyst.set_password('password123')
                analyst.save()
            analyst.roles.set(Role.objects.filter(name='Analyst'))

    def create_groups(self):
        groups_data = [
            ('Customer 1', 'manager1@example.com', 'analyst1@example.com', 'admin@example.com'),
            ('Customer 2', 'manager2@example.com', 'analyst2@example.com'),
            ('Customer 3', 'manager3@example.com', 'analyst3@example.com')
        ]

        for group_name, manager_email, analyst_email, *admin_email in groups_data:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                manager = User.objects.get(email=manager_email)
                analyst = User.objects.get(email=analyst_email)
                group.members.add(manager, analyst)
                if admin_email:
                    admin = User.objects.get(email=admin_email[0])
                    group.members.add(admin)
