from rest_framework import serializers
from sims.models import Project, Machine, Run, Sample, Adapter, Pool, RunPool,\
    AdapterDB
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
    # num_samples = serializers.SerializerMethodField()
    def get_submission_url(self, obj):
        return settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=obj.submission_id)
    # def get_num_samples(self, obj):
    #     return obj.samples.count()
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

class BasePoolSerializer(serializers.ModelSerializer):
#     libraries = LibrarySerializer(many=True, read_only=True)
    class Meta:
        model = Pool
        exclude = []



class RunPoolSerializer(serializers.ModelSerializer):
#     pool = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = RunPool
        exclude = []

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        exclude = []

class LibrarySerializer(SampleSerializer):
    class Meta:
        exclude = []

class AdapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adapter
        exclude = []

class PoolSerializer(BasePoolSerializer):
    samples = SampleSerializer(many=True, read_only=True)
    pools = BasePoolSerializer(many=True, read_only=True)

class RunPoolDetailSerializer(serializers.ModelSerializer):
#     pool = PoolSerializer(read_only=True)
    pool = ModelRelatedField(model=Pool,serializer=PoolSerializer)
    class Meta:
        model = RunPool
        exclude = []
        read_only_fields =('run',)

class RunDetailSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        run_pools = validated_data.pop('run_pools')
        for rp in run_pools:
            run_pool = RunPool.objects.get(run=instance, index=rp['index'])
            run_pool.pool = rp['pool']
            run_pool.description = rp['description']
            run_pool.save()
        print('Run pools')
        print(run_pools)
        return instance
#         album = Album.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album
    run_pools = RunPoolDetailSerializer(many=True)
    
    class Meta:
        model = Run
        exclude = []

class AdapterDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdapterDB
        exclude = []

