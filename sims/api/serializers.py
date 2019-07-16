from rest_framework import serializers
from sims.models import Project, Machine, Run, Sample, Adapter, Library, Pool, RunPool

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = []
#         read_only_fields = ('id',)

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        exclude = []

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        exclude = []

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        exclude = []

class PoolSerializer(serializers.ModelSerializer):
    libraries = LibrarySerializer(many=True, read_only=True)
#     pools = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = Pool
        exclude = []

class RunPoolSerializer(serializers.ModelSerializer):
#     pool = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = RunPool
        exclude = []

class RunDetailSerializer(serializers.ModelSerializer):
    run_pools = RunPoolSerializer(read_only=True, many=True)
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



