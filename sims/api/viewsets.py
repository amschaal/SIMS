from rest_framework import viewsets, status
from sims.api.serializers import PoolListSerializer, ProjectDetailSerializer, SampleDetailSerializer, SubmissionSerializer, LibrarySerializer, RunSerializer,RunDetailSerializer, MachineSerializer,\
    ProjectSerializer, SampleSerializer, PoolSerializer, \
    AdapterSerializer, RunPoolSerializer, RunPoolDetailSerializer,\
    AdapterDBSerializer, ImporterDetailSerializer, ImporterSerializer, SubmissionTypeSerializer
from sims.coreomics.api import get_submission_types
from sims.id_utils import SampleNameGenerator
from sims.models import Submission, Run, Machine, Project, Sample, Pool, Adapter,\
    RunPool, AdapterDB, SubmissionType, Importer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.conf import settings
from sims.submission import SubmissionImporter
from tools.barcodes import get_all_conflicts
from django.utils import timezone
from . import mixins

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
        importer_id = request.data.get('importer')
        importer = Importer.objects.get(id=importer_id)
        if getattr(instance,'project',None):
            raise APIException('Submission has already been processed')
        # instance.process(importer)
        project, pools, samples = instance.process(importer)
        return Response({'project': ProjectSerializer(project).data, 'new_pools': PoolSerializer(pools, many=True).data, 'new_samples': SampleSerializer(samples, many=True).data})
    @action(detail=True, methods=['post'])
    def unimport(self, request, pk=None):
        instance = self.get_object()
        instance.unimport()
        return Response({'message': 'Submission has been unimported', 'submission': SubmissionSerializer(instance).data})
class ProjectViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet, mixins.JSONSchemaMixin):
    serializer_class = ProjectSerializer
    filterset_fields = {
        'id':['icontains','exact'],
        'samples__id': ['exact'],
        'samples__id': ['exact'],
        'samples__pools__id': ['exact'],
        'samples__pools__run_pools__run__id': ['exact'],
        'type__id': ['exact']
        }
    search_fields = ('id', 'submission__id', 'pi_first_name', 'pi_last_name', 'pi_email', 'first_name', 'last_name', 'email')
    ordering_fields = ['id', 'submitted', 'submission_id', 'created']
    queryset = Project.objects.distinct()
    action_serializers = {
        'retrieve': ProjectDetailSerializer,
        'list': ProjectSerializer,
        'create': ProjectSerializer,
        'update': ProjectSerializer
    }
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
    @action(detail=True, methods=['post'])
    def validate_samples(self, request, pk=None, save=False):
        project = self.get_object()
        generator = SampleNameGenerator(project)
        sample_dict = dict((s.id, s) for s in project.samples.all())
        sample_data = request.data.get('data')
        # samples = SampleSerializer(data=sample_data, many=True)
        # valid = samples.is_valid()
        errors = {}
        valid = True
        samples = []
        for i, s in enumerate(sample_data):
            id = s.get('id')
            if id:
                instance = sample_dict.get(id)
                sample = SampleSerializer(instance=instance, data=s)
            else:
                sample = SampleSerializer(data=s, generator=generator)
            if not sample.is_valid():
                valid = False
                errors[i] = sample.errors
            samples.append(sample)
        if not errors and save:
            for s in samples:
                s.save()
            return Response([s.data for s in samples])
        return Response({'data': sample_data, 'is_valid': valid, 'errors': errors, }, status= status.HTTP_400_BAD_REQUEST if errors else status.HTTP_200_OK)
    @action(detail=True, methods=['post'])
    def update_samples(self, request, pk=None, save=False):
        return self.validate_samples(request, pk, True)
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

class SampleViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet, mixins.JSONSchemaMixin):
    action_serializers = {
        'retrieve': SampleDetailSerializer
    }
    filterset_fields = {
        'name':['icontains','exact'],
        'id':['icontains','exact'],
        'project__id':['icontains','exact'],
        'pools__id': ['exact'],
        'pools__run_pools__run__id': ['exact'],
        'samples__id': ['exact'],
        'submission__id': ['exact'],
        'type__id': ['exact']
        }
    search_fields = ('id', 'project__id')
    serializer_class = SampleSerializer
    queryset = Sample.objects.distinct()


class LibraryViewSet(viewsets.ModelViewSet, mixins.JSONSchemaMixin):
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

class PoolViewSet(viewsets.ModelViewSet, mixins.JSONSchemaMixin):
    filterset_fields = {
        'name':['icontains','exact'],
        'samples__id':['exact'],
        'samples__id':['exact'],
        'samples__project__id':['exact'],
        'pooled__id':['exact'],
        'pools__id':['exact'],
        'run_pools__run__id':['exact'],
        'project__id':['icontains','exact'],
        'submission__id': ['exact'],
        'locked': ['isnull'],
        'type__id': ['exact']
        }
    search_fields = ('id', 'name', 'samples__id', 'samples__project__id', 'type__name')
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
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        # if pool.locked:
        #     return Respon
        pool = self.get_object()
        pool.locked = timezone.now()
        pool.save()
        return Response(PoolSerializer(instance=pool).data)
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        pool = self.get_object()
        if pool.pooled.exists() or pool.run_pools.exists():
            return Response({'detail': 'Pool cannot be unlocked if it is in another pool or run.'}, status=status.HTTP_403_FORBIDDEN)
        pool.locked = None
        pool.save()
        return Response(PoolSerializer(instance=pool).data)
    @action(detail=True, methods=['GET'])
    def samples(self, request, pk=None):
        pool = self.get_object()
        return Response(SampleSerializer(pool.get_all_samples(), many=True).data)
    @action(detail=True, methods=['GET'])
    def check_barcodes(self,request, pk=None):
        pool = self.get_object()
        conflicts = get_all_conflicts(SampleSerializer(pool.get_all_samples(), many=True).data)
        return Response({'conflicts': conflicts})
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

class RunViewSet(mixins.ActionSerializerMixin, mixins.JSONSchemaMixin, viewsets.ModelViewSet):
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
        'type__id': ['exact']
        }#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    ordering_fields = ['created', 'name', 'machine__name']
    search_fields = ('name', 'description', 'machine__name')
    def get_queryset(self):
        if self.action == 'retrieve':
            return Run.objects.distinct().prefetch_related('run_pools', 'run_pools__pool__samples')
        return Run.objects.distinct()

class RunPoolViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet):
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

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    model = Machine
    filterset_fields = {'name':['icontains'], 'description':['icontains'], 'type__id': ['exact']}
#     filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Machine.objects.distinct()

class SubmissionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubmissionTypeSerializer
    model = SubmissionType
    queryset = SubmissionType.objects.all()
    ordering_fields = ['name', 'lab_id', 'sort_order'],
    search_fields = ('name', 'description', 'prefix')
    @action(detail=True, methods=['post'])
    def update_mapping(self, request, pk=None):
        st = self.get_object()
        mapping = request.data.get('mapping')
        st.mapping = mapping
        st.save()
        return Response(mapping)

class ImporterViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet):
    serializer_class = ImporterSerializer
    action_serializers = {
        'retrieve': ImporterDetailSerializer,
        'list': ImporterSerializer,
        'create': ImporterDetailSerializer,
        'update': ImporterDetailSerializer
    }
    model = Importer
    queryset = Importer.objects.all()
    filterset_fields = {'submission_type':['exact']}
    # ordering_fields = ['name', 'submission_type', 'model_type'],
    # search_fields = ('name', 'description')
    # @action(detail=True, methods=['post'])
    # def update_mapping(self, request, pk=None):
    #     st = self.get_object()
    #     mapping = request.data.get('mapping')
    #     st.mapping = mapping
    #     st.save()
    #     return Response(mapping)