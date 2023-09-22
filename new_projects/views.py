from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from .models import Projects
from .serializers import CreateProjectSerializer, ProjectsSerializer

class ProjectViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'updated_at', 'property_type']
    filterset_class = []
    permission_classes = []

    # @action(detail=False, methods=['GET'])
    # def agent_properties(self, request):
    #     user = self.request.user
    #     if user.is_staff or (hasattr(user, 'users') and hasattr(user.users, 'agent')):
    #         if user.is_staff:
    #             properties = self.get_queryset()
    #         else:
    #             properties = self.get_queryset().filter(agent__agent_user__user=user)
    #         serializer = self.get_serializer(properties, many=True)
    #         return Response(serializer.data)
    #     return HttpResponse("Unauthorized", status=401)

    # def destroy(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated and self.request.user.is_staff or self.request.user.users.agent:
    #         return super().destroy(request, *args, **kwargs)
    #     return Response({'message': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['GET'])
    # def detail_property(self, request, pk=None):
    #     project = self.get_object()
    #     serializer = ProjectsSerializer(project)
    #     return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def create_project(self, request):
        if self.request.user:
            serializer = CreateProjectSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                project = serializer.save()
                return Response(ProjectsSerializer(instance=project, context={'request': request}).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
