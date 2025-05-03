# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Task
from .serializers import TaskSerializer
import logging

# Get a logger instance
logger = logging.getLogger("tasks")


class TaskListCreateView(generics.ListCreateAPIView):
    """
    API view to list all tasks or create a new task.
    """

    serializer_class = TaskSerializer
    queryset = Task.objects.all()  # Define queryset at class level

    def get_queryset(self):
        """
        Optionally filter tasks by status if provided in query parameters.
        """
        queryset = super().get_queryset()
        status_param = self.request.query_params.get("status")

        if status_param:
            logger.info(f"Filtering tasks by status: {status_param}")
            return queryset.filter(status=status_param)

        logger.info("Retrieving all tasks")
        return queryset

    def perform_create(self, serializer):
        """
        Log task creation and save the new task.
        """
        logger.info(f"Creating new task: {serializer.validated_data.get('title')}")
        serializer.save()


class TaskDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific task by ID.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Log task retrieval and return the task details.
        """
        try:
            instance = self.get_object()
            logger.info(f"Retrieved task: {instance.title} (ID: {instance.id})")
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving task with ID {kwargs.get('pk')}: {str(e)}")
            return Response(
                {"error": "Task not found or could not be retrieved"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TaskCompleteView(generics.GenericAPIView):
    """
    API view to mark a task as completed.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        Mark a task as completed and set the completion timestamp.

        Returns:
            - 200 OK if task is successfully marked as completed
            - 400 Bad Request if task is already completed
            - 404 Not Found if task doesn't exist
        """
        try:
            task = self.get_object()

            # Check if task is already completed
            if task.status == "completed":
                logger.warning(
                    f"Attempt to complete already completed task: {task.title} (ID: {task.id})"
                )
                return Response(
                    {"error": "Task is already completed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            logger.info(f"Marking task {task.title} (ID: {task.id}) as completed")

            task.status = "completed"
            task.completed_at = now()
            task.save()

            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error completing task with ID {kwargs.get('pk')}: {str(e)}")
            return Response(
                {"error": "Task not found or could not be completed"},
                status=status.HTTP_404_NOT_FOUND,
            )
