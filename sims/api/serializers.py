from rest_framework import serializers
from sims.models import Submission, Machine, Run, Lane, Sample, Adapter, Library, Pool,\
    LanePool

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
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



class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        exclude = []

class LanePoolSerializer(serializers.ModelSerializer):
    pools = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = LanePool
        exclude = []

class RunDetailSerializer(serializers.ModelSerializer):
    lanes = LanePoolSerializer(read_only=True, many=True)
    class Meta:
        model = Run
        exclude = []

class LaneSerializer(serializers.ModelSerializer):
    lane_pools = LanePoolSerializer(read_only=True, many=True)
    class Meta:
        model = Lane
        exclude = []

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        exclude = []

class AdapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adapter
        exclude = []

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        exclude = []

