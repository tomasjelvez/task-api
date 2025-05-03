# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get("status")
        if status_param:
            return Task.objects.filter(status=status_param)
        return Task.objects.all()


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCompleteView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["post", "put", "patch"]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "completed"
        task.completed_at = now()
        task.save()
        return Response(TaskSerializer(task).data)
