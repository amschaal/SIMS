from rest_framework import viewsets, status
from sims.api.serializers import SubmissionSerializer, LibrarySerializer, RunSerializer,RunDetailSerializer, MachineSerializer,\
    ProjectSerializer, SampleSerializer, PoolSerializer, \
    AdapterSerializer, RunPoolSerializer, RunPoolDetailSerializer,\
    AdapterDBSerializer
from sims.models import Submission, Run, Machine, Project, Sample, Pool, Adapter,\
    RunPool, AdapterDB
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.conf import settings
from sims.submission import SubmissionImporter
from tools.barcodes import get_all_conflicts

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    filterset_fields = {
        'id':['icontains','exact'],
        'samples__id': ['exact'],
        'samples__id': ['exact'],
        'samples__pools__id': ['exact'],
        'samples__pools__run_pools__run__id': ['exact']
        }
    search_fields = ('id', 'submission_id', 'pi_first_name', 'pi_last_name', 'pi_email', 'first_name', 'last_name', 'email')
    ordering_fields = ['id', 'submitted', 'submission_id', 'created']
    queryset = Submission.objects.distinct()
    @action(detail=False, methods=['get','post'])
    def import_submission(self, request):
        id = request.data.get('id').strip()
#         url = settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=id)
        try:
            submission_importer = SubmissionImporter.get_submission(id)
        except Exception as e:
            return Response({'message': 'Error: unable to retrieve submission with ID "{}": {}'.format(id,e)},status=status.HTTP_400_BAD_REQUEST)
        try:
            submission = submission_importer.import_submission()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'id':id,'submission':submission_importer._data, 'import': SubmissionSerializer(submission).data})
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        instance = self.get_object()
        if getattr(instance,'project',None):
            raise APIException('Submission has already been processed')
        project, pools, samples = instance.process()
        return Response({'project': ProjectSerializer(project).data, 'new_pools': PoolSerializer(pools, many=True).data, 'new_samples': SampleSerializer(samples, many=True).data})

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filterset_fields = {
        'id':['icontains','exact'],
        'samples__id': ['exact'],
        'samples__id': ['exact'],
        'samples__pools__id': ['exact'],
        'samples__pools__run_pools__run__id': ['exact']
        }
    search_fields = ('id', 'submission_id', 'pi_first_name', 'pi_last_name', 'pi_email', 'first_name', 'last_name', 'email')
    ordering_fields = ['id', 'submitted', 'submission_id', 'created']
    queryset = Project.objects.distinct()
    @action(detail=True, methods=['post'])
    def update_samples(self, request, pk=None):
        project = self.get_object()
#         url = settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=id)
        try:
            submission_importer = SubmissionImporter.get_submission(project.submission_id)
        except:
            return Response({'message': 'Error: unable to retrieve submission with ID "{0}"'.format(id)},status=status.HTTP_400_BAD_REQUEST)
        try:
            samples = submission_importer.update_samples(project, import_only=True)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'project': ProjectSerializer(project).data, 'new_samples': SampleSerializer(samples, many=True).data})
    # @action(detail=True, methods=['post'])
    # def process_samples(self, request, pk=None):
    #     project = self.get_object()
    #     if hasattr(project, 'dataimport'):
    #         raise APIException('Project already has data import')
    #     data_import = DataImport(project=project)
    #     data_import.save()
    #     pools, samples = data_import.process()
    #     return Response({'project': ProjectSerializer(project).data, 'new_pools': PoolSerializer(pools, many=True).data, 'new_samples': SampleSerializer(samples, many=True).data})
    #     # return Response({'samples':SampleSerializer(samples, many=True).data})

class SampleViewSet(viewsets.ModelViewSet):
    filterset_fields = {
        'name':['icontains','exact'],
        'id':['icontains','exact'],
        'project__id':['icontains','exact'],
        'pools__id': ['exact'],
        'pools__run_pools__run__id': ['exact'],
        'samples__id': ['exact'],
        'submission__id': ['exact']
        }
    search_fields = ('id', 'project__id')
    serializer_class = SampleSerializer
    queryset = Sample.objects.distinct()

class LibraryViewSet(viewsets.ModelViewSet):
    filterset_fields = {
        'id':['icontains','exact'],
        'name':['icontains','exact'],
        'id':['icontains','exact'],
        'project__id':['icontains','exact'],
        'pools__id': ['exact'],
        'pools__run_pools__run__id': ['exact'],
        'submission__id': ['exact']
        }
    search_fields = ('id', 'project__id', 'barcode')
    serializer_class = LibrarySerializer
    queryset = Sample.objects.select_related('sample', 'sample__project').filter(physical_type=Sample.TYPE_LIBRARY).distinct()
    @action(detail=False, methods=['get','post'])
    def check_adapters(self, request):
        libs = request.data.get('libraries',[]) # [{'id': 'library_id', 'adapter_db': '...', 'adapter': '...'}, ...]
        search_adapters = request.data.get('search_adapters', False)
        min_distance = request.data.get('min_distance',2)
        libraries = []
        errors = {}
        for l in libs:
            if not 'id' in l:
                continue
            lib = {'id': l['id']}
            if 'barcodes' in l:
                lib['barcodes'] =  l['barcodes']
                libraries.append(lib)
            elif 'adapter_db' in l and 'adapter' in l:
                try:
                    lib['barcodes'] = Adapter.objects.get(db__id=l['adapter_db'], name=l['adapter']).barcodes
                    libraries.append(lib)
                except Adapter.DoesNotExist:
                    errors[l['id']] = 'No adapter found for library "{}" for DB "{}" and adapter ""'.format(l['id'], l['adapter_db'], l['adapter'])
            elif 'adapter_id' in l:
                try:
                    lib['barcodes'] = Adapter.objects.get(id=l['adapter_id']).barcodes
                    libraries.append(lib)
                except Adapter.DoesNotExist:
                    errors[l['id']] = 'No adapter found for library "{}" for adapter_id ""'.format(l['id'], l['adapter_id'])
            else:
                errors[l['id']] = 'Library "{}" must have either "barcodes", "adapter_id", or "adapter_db" and "adapter" properties'.format(l['id'])
                continue
        return self.check_compatibility(libraries, min_distance, errors)
    @action(detail=False, methods=['get','post'])
    def check_libraries(self, request):
        libs = request.data.get('library_ids',[])
        min_distance = request.data.get('min_distance',2)
        libraries = Sample.objects.filter(id__in=libs)
        return self.check_compatibility(LibrarySerializer(libraries, many=True).data, min_distance=min_distance)
    def check_compatibility(self, libraries, min_distance=2, errors={}):
        conflicts = get_all_conflicts(libraries, min_distance=min_distance)
        return Response({'conflicts': conflicts, 'errors': errors})

class PoolViewSet(viewsets.ModelViewSet):
    filterset_fields = {
        'name':['icontains','exact'],
        'samples__id':['exact'],
        'samples__id':['exact'],
        'samples__project__id':['exact'],
        'pooled__id':['exact'],
        'pools__id':['exact'],
        'run_pools__run__id':['exact']
        }
    serializer_class = PoolSerializer
    queryset = Pool.objects.distinct()
    @action(detail=True, methods=['get','post'])
    def add_samples(self, request, pk=None):
        return self.update_samples(request, 'add')
    @action(detail=True, methods=['get','post'])
    def remove_samples(self, request, pk=None):
        return self.update_samples(request, 'remove')
    def update_samples(self, request, action):
        pool = self.get_object()
        data = request.data
        samples = list(Sample.objects.filter(id__in=data.get('samples',[])))
        samples += list(Sample.objects.filter(project__id__in=data.get('projects',[])))
        if action == 'add':
            pool.samples.add(*samples)
        elif action == 'remove':
            pool.samples.remove(*samples)
        return Response({'samples': SampleSerializer(pool.samples.all(),many=True).data})
    @action(detail=True, methods=['get','post'])
    def add_pools(self, request, pk=None):
        return self.update_pools(request, 'add')
    @action(detail=True, methods=['get','post'])
    def remove_pools(self, request, pk=None):
        return self.update_pools(request, 'remove')
    def update_pools(self, request, action):
        pool = self.get_object()
        data = request.data
        pools = list(Pool.objects.filter(id__in=data.get('pools',[])))
        if action == 'add':
            pool.pools.add(*pools)
        elif action == 'remove':
            pool.pools.remove(*pools)
        return Response({'pools': PoolSerializer(pool.pools.all(),many=True).data})

class AdapterDBViewset(viewsets.ReadOnlyModelViewSet):
    queryset = AdapterDB.objects.distinct()
    serializer_class = AdapterDBSerializer
    filterset_fields = {
        'name':['icontains','exact'],
        'id':['icontains','exact'],
        'description':['icontains']
        }
    search_fields = ('name', 'id')

class AdapterViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_fields = {
        'name':['icontains','exact']
#         'barcodes':['icontains','exact']
        }
    search_fields = ('name',)
    serializer_class = AdapterSerializer
    queryset = Adapter.objects.distinct()
    lookup_field = 'name'
    def get_queryset(self):
        return viewsets.ReadOnlyModelViewSet.get_queryset(self).filter(db=self.kwargs.get('db'))
    def get_object(self):
        return viewsets.ReadOnlyModelViewSet.get_object(self)
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
        'create': RunSerializer,
        'update': RunDetailSerializer
    }
    serializer_class = RunSerializer
    queryset = Run.objects.distinct()
    filterset_fields = {
        'name':['icontains'],
        'machine__id':['exact'],
        'machine__name':['icontains'],
        'description':['icontains'],
        'run_pools__pool__id':['exact'],
        'run_pools__pool__samples__id':['exact'],
        'run_pools__pool__samples__sample__id':['exact'],
        'run_pools__pool__samples__sample__project__id':['exact'],
        }#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    ordering_fields = ['created', 'name', 'machine__name']
    search_fields = ('name', 'description', 'machine__name')
    def get_queryset(self):
        if self.action == 'retrieve':
            return Run.objects.distinct().prefetch_related('run_pools', 'run_pools__pool__samples')
        return Run.objects.distinct()
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)

class RunPoolViewSet(viewsets.ModelViewSet):
    filterset_fields = {'run__id':['exact']
                     }
    serializer_class = RunPoolSerializer
    queryset = RunPool.objects.distinct().order_by('run', 'index')
    action_serializers = {
        'retrieve': RunPoolDetailSerializer,
        'list': RunPoolSerializer,
        'create': RunPoolSerializer,
        'update': RunPoolSerializer
    }
    def get_queryset(self):
        if self.action == 'retrieve':
            return RunPool.objects.distinct().prefetch_related('pool__samples')
        return RunPool.objects.distinct()
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    model = Machine
    filterset_fields = {'name':['icontains'],'description':['icontains']}
#     filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Machine.objects.distinct()
