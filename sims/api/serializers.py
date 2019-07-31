from rest_framework import serializers
from sims.models import Project, Machine, Run, Sample, Adapter, Library, Pool, RunPool
from django.conf import settings

#Allows Creation/Updating of related model fields with OBJECT instead of just id
#usage field_name = ModelRelatedField(model=Sample,serializer=SampleSerializer)
class ModelRelatedField(serializers.RelatedField):
    model = None
    pk = 'id'
    serializer = None
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', self.model)
        self.pk = kwargs.pop('pk', self.pk)
        self.serializer = kwargs.pop('serializer', self.serializer)
        assert self.model is not None, (
            'Must set model for ModelRelatedField'
        )
        assert self.serializer is not None, (
            'Must set serializer for ModelRelatedField'
        )
        self.queryset = kwargs.pop('queryset', self.model.objects.all())
        super(ModelRelatedField, self).__init__(**kwargs)
    def to_internal_value(self, data):
        if isinstance(data, int) or isinstance(data, str):
            kwargs = {self.pk:data}
            return self.model.objects.get(**kwargs)
        if data.get(self.pk,None):
            return self.model.objects.get(id=data['id'])
        return None
    def to_representation(self, value):
        return self.serializer(value).data

class ProjectSerializer(serializers.ModelSerializer):
    submission_url = serializers.SerializerMethodField()
    def get_submission_url(self, obj):
        return settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=obj.submission_id)
    class Meta:
        model = Project
        exclude = []
#         read_only_fields = ('id',)

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        exclude = []

class RunSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    def get_machine_name(self, obj):
        return obj.machine.name
    class Meta:
        model = Run
        exclude = []

class LibrarySerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    def get_project(self, obj):
        return obj.sample.project_id
    class Meta:
        model = Library
        exclude = []

class BasePoolSerializer(serializers.ModelSerializer):
#     libraries = LibrarySerializer(many=True, read_only=True)
    class Meta:
        model = Pool
        exclude = []

class PoolSerializer(BasePoolSerializer):
    libraries = LibrarySerializer(many=True, read_only=True)
    pools = BasePoolSerializer(many=True, read_only=True)

class RunPoolSerializer(serializers.ModelSerializer):
#     pool = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = RunPool
        exclude = []

class RunPoolDetailSerializer(serializers.ModelSerializer):
    pool = PoolSerializer(read_only=True)
    class Meta:
        model = RunPool
        exclude = []

class RunDetailSerializer(serializers.ModelSerializer):
    run_pools = RunPoolDetailSerializer(read_only=True, many=True)
    class Meta:
        model = Run
        exclude = []

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        exclude = []

class AdapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adapter
        exclude = []



