from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Task


class TodoAPISecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="alice", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="bob", password="StrongPass123!")
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_registration_hashes_password(self):
        response = self.client.post(
            "/api/register/",
            {"username": "charlie", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="charlie")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertNotEqual(user.password, "StrongPass123!")
        self.assertNotIn("password", response.data)

    def test_login_returns_token_for_valid_credentials(self):
        response = self.client.post(
            "/api/login/",
            {"username": "alice", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_tasks_require_authentication(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 401)

    def test_task_is_assigned_to_authenticated_user(self):
        self.authenticate(self.token)
        response = self.client.post(
            "/api/tasks/",
            {"title": "Private task", "description": "Alice's task"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get(pk=response.data["id"])
        self.assertEqual(task.user, self.user)

    def test_user_cannot_read_another_users_task(self):
        task = Task.objects.create(user=self.other_user, title="Bob private task")
        self.authenticate(self.token)
        response = self.client.get(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_modify_another_users_task(self):
        task = Task.objects.create(user=self.other_user, title="Bob private task")
        self.authenticate(self.token)
        response = self.client.put(
            f"/api/tasks/{task.id}/",
            {"title": "Tampered", "description": "No", "completed": True},
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertEqual(task.title, "Bob private task")

    def test_user_cannot_delete_another_users_task(self):
        task = Task.objects.create(user=self.other_user, title="Bob private task")
        self.authenticate(self.token)
        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=task.id).exists())

    def test_task_user_field_cannot_be_changed_by_client(self):
        self.authenticate(self.token)
        response = self.client.post(
            "/api/tasks/",
            {"title": "Owned task", "user": self.other_user.id},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get(pk=response.data["id"])
        self.assertEqual(task.user, self.user)
