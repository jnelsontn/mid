from rest_framework.response import Response
from rest_framework.renderers import *
from rest_framework import viewsets
from django.http import JsonResponse
from django.db.models import F
from .serializers import *
from .models import *


def get_max_value():
    return max(sorted(list(Features.objects.values_list('priority', flat=True))))


def return_max_value(request):
    if request.is_ajax():
        max_value = get_max_value()
        return JsonResponse(max_value, safe=False)


class FeaturesViewSet(viewsets.ModelViewSet):
    """
    No Custom Methods... Just over-ride and get
    what we need.
    We can use the Django ORM to bulk update all obj
    returned from querysets.
    """

    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'success.html'

    def get_queryset(self):
        """
        Allow a search based on project when id when the 'project_id' url
        param is used
        :return:
        """
        queryset = Features.objects.all()
        project = self.request.query_params.get('project_id', None)
        if project is not None:
            return Features.objects.filter(project=project)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        if self.request.query_params.get('create', None):
            return Response({'serializer': serializer}, template_name='feature_form.html')
        return super(FeaturesViewSet, self).list(request)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = FeaturesSerializer(instance=obj, context={'request': request})
        if request.accepted_renderer.format == 'html':
            return Response({
                'feature_obj': obj,
                'features_serializer': serializer,
            }, template_name='update_feature_form.html')
        return super(FeaturesViewSet, self).retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        requested = int(self.request.data['priority'])
        max_value = get_max_value()

        if requested < 1 or requested > max_value:
            return JsonResponse('Invalid Priority', safe=False)
        else:
            search = self.get_queryset().filter(priority__gte=requested)
            search.update(priority=F('priority') + 1)

            serializer.save()

    def perform_update(self, serializer):
        requested = int(self.request.data['priority'])
        current = self.get_object().priority
        max_value = get_max_value()

        if requested < 1 or requested > max_value:
            return JsonResponse('Invalid Priority', safe=False)

        if requested < current:
            search = self.get_queryset().filter(priority__lt=current).filter(priority__gte=requested)
            search.update(priority=F('priority') + 1)

        else:
            search = self.get_queryset().filter(priority__gt=current).filter(priority__lte=requested)
            search.update(priority=F('priority') - 1)

        serializer.save()

    def perform_destroy(self, serializer):
        current = self.get_object().priority

        search = self.get_queryset().filter(priority__gt=current)
        search.update(priority=F('priority') - 1)

        serializer.delete()


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer}, template_name='client_form.html')
        return super(ClientsViewSet, self).list(request, *args, **kwargs)


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get_queryset(self):
        """
        Allow a search based on client when id when the 'client_id' url
        param is used
        :return:
        """
        queryset = Projects.objects.all()
        specific_client = self.request.query_params.get('client_id', None)
        if specific_client is not None:
            return Projects.objects.filter(client_id=specific_client)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer}, template_name='project_form.html')
        return super(ProjectsViewSet, self).list(request, *args, **kwargs)


class ProductAreaViewSet(viewsets.ModelViewSet):

    queryset = ProductArea.objects.all()
    serializer_class = ProductAreaSerializer
