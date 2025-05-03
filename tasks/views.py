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
    serializer_class = TaskSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get("status")
        logger.info(f"Filtering tasks by status: {status_param}")
        if status_param:
            return Task.objects.filter(status=status_param)
        return Task.objects.all()

    def perform_create(self, serializer):
        logger.info(f"Creating new task: {serializer.validated_data.get('title')}")
        return super().perform_create(serializer)


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Retrieved task: {instance.title} (ID: {instance.id})")
        return super().retrieve(request, *args, **kwargs)


class TaskCompleteView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["post", "put", "patch"]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        logger.info(f"Marking task {task.title}(ID: {task.id}) as completed")
        task.status = "completed"
        task.completed_at = now()
        task.save()
        return Response(TaskSerializer(task).data)
