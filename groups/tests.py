from django.test import TestCase
from django.urls import reverse
from users.models import User, Role, Permission
from groups.models import Group


class GroupViewTest(TestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@example.com', password='password123', is_staff=True)

        # Get or create required permissions
        self.edit_groups_permission, _ = Permission.objects.get_or_create(name='edit_groups')
        self.view_groups_permission, _ = Permission.objects.get_or_create(name='view_groups')
        self.delete_groups_permission, _ = Permission.objects.get_or_create(name='delete_groups')

        # Get or create admin role and assign permissions to the role
        self.admin_role, _ = Role.objects.get_or_create(name='Admin')
        self.admin_role.permissions.add(self.edit_groups_permission)
        self.admin_role.permissions.add(self.view_groups_permission)
        self.admin_role.permissions.add(self.delete_groups_permission)

        # Assign role to admin user
        self.admin_user.roles.add(self.admin_role)

    def test_group_list_view(self):
        self.client.login(email=self.admin_user.email, password='password123')
        Group.objects.create(name='Group 1')
        Group.objects.create(name='Group 2')

        response = self.client.get(reverse('group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Group 1')
        self.assertContains(response, 'Group 2')

    def test_group_detail_view(self):
        self.client.login(email=self.admin_user.email, password='password123')
        group = Group.objects.create(name='Group Detail')
        group.members.add(self.admin_user)

        response = self.client.get(reverse('group_detail', args=[group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Group Detail')

    def test_group_create_view(self):
        self.client.login(email=self.admin_user.email, password='password123')
        response = self.client.post(reverse('group_add'), {'name': 'New Group', 'members': [self.admin_user.id]})
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        new_group = Group.objects.get(name='New Group')
        self.assertEqual(new_group.name, 'New Group')

    def test_group_edit_view(self):
        self.client.login(email=self.admin_user.email, password='password123')
        group = Group.objects.create(name='Old Group')
        group.members.add(self.admin_user)

        response = self.client.post(reverse('group_edit', args=[group.id]),
                                    {'name': 'Updated Group', 'members': [self.admin_user.id]})
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        updated_group = Group.objects.get(id=group.id)
        self.assertEqual(updated_group.name, 'Updated Group')

    def test_group_delete_view(self):
        self.client.login(email=self.admin_user.email, password='password123')
        group = Group.objects.create(name='Group to Delete')
        group.members.add(self.admin_user)

        response = self.client.post(reverse('group_delete', args=[group.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(id=group.id)

    def test_group_create_view_get(self):
        self.client.login(email=self.admin_user.email, password='password123')
        response = self.client.get(reverse('group_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_form.html')

    def test_group_edit_view_get(self):
        self.client.login(email=self.admin_user.email, password='password123')
        group = Group.objects.create(name='Old Group')
        group.members.add(self.admin_user)

        response = self.client.get(reverse('group_edit', args=[group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_form.html')

    def test_group_delete_view_get(self):
        self.client.login(email=self.admin_user.email, password='password123')
        group = Group.objects.create(name='Group to Delete')
        group.members.add(self.admin_user)

        response = self.client.get(reverse('group_delete', args=[group.id]))
        self.assertEqual(response.status_code, 405)  # Should not allow GET requests for delete
