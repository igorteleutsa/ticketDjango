# In users/tests.py
from django.test import TestCase
from django.urls import reverse
from users.models import User, Role, Permission
from users.forms import UserForm, UserRegistrationForm


class UserViewTest(TestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            email="admin@example.com", password="complex_password123", is_staff=True
        )

        # Get or create required permissions
        self.edit_users_permission, _ = Permission.objects.get_or_create(
            name="edit_users"
        )
        self.view_users_permission, _ = Permission.objects.get_or_create(
            name="view_users"
        )
        self.delete_users_permission, _ = Permission.objects.get_or_create(
            name="delete_users"
        )

        # Get or create admin role and assign permissions to the role
        self.admin_role, _ = Role.objects.get_or_create(name="Admin")
        self.admin_role.permissions.add(self.edit_users_permission)
        self.admin_role.permissions.add(self.view_users_permission)
        self.admin_role.permissions.add(self.delete_users_permission)

        # Assign role to admin user
        self.admin_user.roles.add(self.admin_role)

    def test_register_view(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "newuser@example.com",
                "password1": "complex_password123",  # Use a more complex password
                "password2": "complex_password123",
                "roles": [self.admin_role.id],  # Provide the roles field
            },
        )
        if response.status_code == 200:
            print(response.context["form"].errors)  # Print form errors if any
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        new_user = User.objects.get(email="newuser@example.com")
        self.assertEqual(new_user.email, "newuser@example.com")

    def test_logout_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

    def test_user_list_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        User.objects.create_user(
            email="user1@example.com", password="complex_password123"
        )
        User.objects.create_user(
            email="user2@example.com", password="complex_password123"
        )

        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1@example.com")
        self.assertContains(response, "user2@example.com")

    def test_user_detail_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        user = User.objects.create_user(
            email="userdetail@example.com", password="complex_password123"
        )

        response = self.client.get(reverse("user_detail", args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "userdetail@example.com")

    def test_user_create_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        response = self.client.post(
            reverse("user_add"),
            {
                "email": "createuser@example.com",
                "password": "complex_password123",
                "roles": [self.admin_role.id],  # Provide the roles field
            },
        )
        if response.status_code == 200:
            print(response.context["form"].errors)  # Print form errors if any
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        new_user = User.objects.get(email="createuser@example.com")
        self.assertEqual(new_user.email, "createuser@example.com")

    def test_user_edit_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        user = User.objects.create_user(
            email="edituser@example.com", password="complex_password123"
        )

        response = self.client.post(
            reverse("user_edit", args=[user.id]),
            {
                "email": "updateduser@example.com",
                "password": "complex_password123",
                "roles": [self.admin_role.id],  # Provide the roles field
            },
        )
        if response.status_code == 200:
            print(response.context["form"].errors)  # Print form errors if any
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.email, "updateduser@example.com")

    def test_user_delete_view(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        user = User.objects.create_user(
            email="deleteuser@example.com", password="complex_password123"
        )

        response = self.client.post(reverse("user_delete", args=[user.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after success

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user.id)

    def test_user_create_view_get(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        response = self.client.get(reverse("user_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_user_edit_view_get(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        user = User.objects.create_user(
            email="edituser@example.com", password="complex_password123"
        )

        response = self.client.get(reverse("user_edit", args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_form.html")

    def test_user_delete_view_get(self):
        self.client.login(email=self.admin_user.email, password="complex_password123")
        user = User.objects.create_user(
            email="deleteuser@example.com", password="complex_password123"
        )

        response = self.client.get(reverse("user_delete", args=[user.id]))
        self.assertEqual(
            response.status_code, 405
        )  # Should not allow GET requests for delete
