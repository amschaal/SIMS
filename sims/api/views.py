from rest_framework import viewsets
from sims.api.serializers import RunSerializer,RunDetailSerializer, MachineSerializer,\
    ProjectSerializer, SampleSerializer, PoolSerializer, LibrarySerializer,\
    AdapterSerializer
from sims.models import Run, Machine, Project, Sample, Pool, Library, Adapter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from sims.submission import Submission

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filter_fields = {'name':['icontains'],'description':['icontains']}
    queryset = Project.objects.all()
    @action(detail=False, methods=['get','post'])
    def import_submission(self, request):
        data = request.query_params
        url = settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=data.get('id'))
        submission = Submission.get_submission(data.get('id'))
        project = submission.create_project()
        return Response({'id':data,'url':url, 'submission':submission._data, 'project': ProjectSerializer(project).data})

class SampleViewSet(viewsets.ModelViewSet):
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()

class LibraryViewSet(viewsets.ModelViewSet):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()

class PoolViewSet(viewsets.ModelViewSet):
    serializer_class = PoolSerializer
    queryset = Pool.objects.all()
    @action(detail=True, methods=['get','post'])
    def add_libraries(self, request, pk=None):
        return self.update_libraries(request, 'add')
    @action(detail=True, methods=['get','post'])
    def remove_libraries(self, request, pk=None):
        return self.update_libraries(request, 'remove')
    def update_libraries(self, request, action):
        pool = self.get_object()
        data = request.query_params
        libraries = list(Library.objects.filter(id__in=data.getlist('libraries',[])))
        libraries += list(Library.objects.filter(sample__project__id__in=data.getlist('projects',[])))
        if action == 'add':
            pool.libraries.add(*[l for l in libraries])
        elif action == 'remove':
            pool.libraries.remove(*[l for l in libraries])
        return Response({'libraries': LibrarySerializer(pool.libraries.all(),many=True).data})

class AdapterViewSet(viewsets.ModelViewSet):
    serializer_class = AdapterSerializer
    queryset = Adapter.objects.all()
# #@todo: fix this... it isn't being called when used as a mixin
# class ActionSerializerMixin(object):
#     """
#     Provide the following in model for different serializers
#     action_serializers = {
#         'retrieve': MyModelDetailSerializer,
#         'list': MyModelListSerializer,
#         'create': MyModelCreateSerializer
#     }
#     """
#     def get_serializer_class(self):
#         if hasattr(self, 'action_serializers'):
#             if self.action in self.action_serializers.keys():
#                 return self.action_serializers[self.action]
#         return viewsets.ModelViewSet.get_serializer_class(self)


class RunViewSet(viewsets.ModelViewSet):
    action_serializers = {
        'retrieve': RunDetailSerializer,
        'list': RunSerializer,
        'create': RunDetailSerializer,
        'update': RunDetailSerializer
    }
    serializer_class = RunSerializer
    model = Run
    filter_fields = {'name':['icontains'],'machine__name':['icontains'],'description':['icontains'],'lanes__pool__name':['icontains'],'lanes__pool__libraries__sample__id':['exact'],'lanes__pool__id':['exact']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Run.objects.distinct()
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    model = Machine
    filter_fields = {'name':['icontains'],'description':['icontains']}
#     filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Machine.objects.all()
