from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Task


class TaskAPITestCase(TestCase):
    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()

        # Create some test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1", priority="high", status="pending"
        )

        self.task2 = Task.objects.create(
            title="Test Task 2",
            priority="medium",
            status="completed",
            completed_at=timezone.now(),
        )

    def test_list_tasks(self):
        """Test retrieving a list of tasks"""
        url = reverse("task-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both tasks

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status"""
        url = reverse("task-list-create")
        response = self.client.get(f"{url}?status=completed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return only completed task
        self.assertEqual(response.data[0]["title"], "Test Task 2")

    def test_create_task(self):
        """Test creating a new task"""
        url = reverse("task-list-create")
        data = {"title": "New Test Task", "priority": "low", "status": "pending"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data["title"], "New Test Task")

    def test_retrieve_task(self):
        """Test retrieving a single task"""
        url = reverse("task-detail", args=[self.task1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task 1")

    def test_complete_task(self):
        """Test marking a task as completed"""
        url = reverse("task-complete", args=[self.task1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh task from database
        self.task1.refresh_from_db()

        # Check that task is now completed
        self.assertEqual(self.task1.status, "completed")
        self.assertIsNotNone(self.task1.completed_at)
