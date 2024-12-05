from rest_framework import serializers
from djson.models import ModelType
from djson.serializers import DjsonTypeModelSerializer, ModelTypeSerializer

# from djson.fields import JSONSchemaField
# from djson.validators import JsonSchemaValidator
from djson.tests import TEST_SCHEMA
from sims.api.fields import JSONSchemaConverterField
from sims.api.validators import BarcodeValidator
from sims.models import (
    Submission,
    Project,
    Machine,
    Run,
    Sample,
    Adapter,
    Pool,
    RunPool,
    AdapterDB,
    SubmissionType,
    Importer,
)
from django.conf import settings
from django.contrib.auth.models import User

from tools.barcodes import get_all_conflicts


# Allows Creation/Updating of related model fields with OBJECT instead of just id
# usage field_name = ModelRelatedField(model=Sample,serializer=SampleSerializer)
class ModelRelatedField(serializers.RelatedField):
    model = None
    pk = "id"
    serializer = None

    def __init__(self, **kwargs):
        self.model = kwargs.pop("model", self.model)
        self.pk = kwargs.pop("pk", self.pk)
        self.serializer = kwargs.pop("serializer", self.serializer)
        assert self.model is not None, "Must set model for ModelRelatedField"
        assert self.serializer is not None, "Must set serializer for ModelRelatedField"
        self.queryset = kwargs.pop("queryset", self.model.objects.all())
        super(ModelRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, int) or isinstance(data, str):
            kwargs = {self.pk: data}
            return self.model.objects.get(**kwargs)
        if data.get(self.pk, None):
            kwargs = {self.pk: data.get(self.pk)}
            return self.model.objects.get(**kwargs)
        return None

    def to_representation(self, value):
        return self.serializer(value).data


class SubmissionSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    schema = JSONSchemaConverterField()

    class Meta:
        model = Submission
        exclude = []


class ProjectSerializer(DjsonTypeModelSerializer):
    submission_url = serializers.SerializerMethodField()
    submission = SubmissionSerializer(
        read_only=True
    )  #  serializers.SerializerMethodField()

    # num_samples = serializers.SerializerMethodField()
    def get_submission_url(self, obj):
        return settings.SUBMISSION_SYSTEM_URLS["submission"].format(
            id=obj.submission_id
        )

    # def get_data_import(self, obj):
    # return DataImportSerializer(obj.data_import)
    # def get_num_samples(self, obj):
    #     return obj.samples.count()
    class Meta:
        model = Project
        exclude = []
        read_only_fields = ("schema", "submission_data", "submission")


def get_schema_func(validator):
    # raise Exception('get_schema_func', validator.serializer.initial_data)
    return validator.schema if validator.schema else TEST_SCHEMA


class MachineSerializer(DjsonTypeModelSerializer):
    # class MachineSerializer(serializers.ModelSerializer):
    # data = JSONSchemaField(schema=TEST_SCHEMA, required=True)
    # data = JSONSchemaField(required=True, get_schema_func=get_schema_func)
    # data = serializers.JSONField(required=False, validators=[JsonSchemaValidator(schema='sdflsdf')])
    class Meta:
        model = Machine
        exclude = []
        read_only_fields = ("schema",)


class RunSerializer(DjsonTypeModelSerializer):
    # class RunSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()

    def get_machine_name(self, obj):
        return obj.machine.name

    class Meta:
        model = Run
        exclude = []
        read_only_fields = ("schema",)


class BasePoolSerializer(DjsonTypeModelSerializer):
    #     libraries = LibrarySerializer(many=True, read_only=True)
    class Meta:
        model = Pool
        exclude = []
        read_only_fields = ("schema", "submission_data")

class PoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        exclude = ['schema']

class RunPoolSerializer(serializers.ModelSerializer):
    #     pool = PoolSerializer(many=True, read_only=True)
    class Meta:
        model = RunPool
        exclude = []


class SampleNameDefault:
    """
    If a sample name generator is passed to the serializer, get the next sample name as the default.
    """

    requires_context = True

    def __call__(self, serializer_field):
        if hasattr(serializer_field, "parent") and serializer_field.parent.generator:
            return serializer_field.parent.generator.next()


class BarcodeSerializer(serializers.Serializer):
    i5 = serializers.CharField(required=False)
    i7 = serializers.CharField(required=False)
    adapter_db = serializers.CharField(required=False)
    adapter = serializers.CharField(required=False)
    class Meta:
        validators = [BarcodeValidator()]


class SampleSerializer(DjsonTypeModelSerializer):
    name = serializers.CharField(default=SampleNameDefault())
    barcodes = BarcodeSerializer(required=False)

    def __init__(self, instance=None, **kwargs):
        self.generator = kwargs.pop("generator", None)
        super().__init__(instance, **kwargs)

    class Meta:
        model = Sample
        exclude = []
        read_only_fields = ("id", "schema", "submission_data")

class SampleDetailSerializer(SampleSerializer):
    pools = serializers.SerializerMethodField()
    def get_pools(self, obj):
        return PoolListSerializer(obj.get_all_pools(), many=True).data

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
    pool = ModelRelatedField(model=Pool, serializer=PoolSerializer)

    def validate_pool(self, value):
        if isinstance(value, str):
            id = value
        else:
            id = getattr(value, "id")
        if id:
            try:
                pool = Pool.objects.get(id=id)
                if not pool.locked:
                    raise serializers.ValidationError(
                        "Pool must be locked before adding it to a run.".format(id)
                    )
                conflicts = get_all_conflicts(SampleSerializer(pool.get_all_samples(), many=True).data)
                if conflicts:
                    raise serializers.ValidationError(
                        "Pool has barcode conflicts"
                    )
            except Pool.DoesNotExist:
                raise serializers.ValidationError(
                    "Pool with id {} does not exist".format(id)
                )
        return value

    class Meta:
        model = RunPool
        exclude = []
        read_only_fields = ("run",)


class RunDetailSerializer(DjsonTypeModelSerializer):
    # class RunDetailSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        run_pools = validated_data.pop("run_pools")
        for rp in run_pools:
            run_pool = RunPool.objects.get(run=instance, index=rp["index"])
            run_pool.pool = rp["pool"]
            run_pool.description = rp["description"]
            run_pool.save()
        print("Run pools")
        print(run_pools)
        return super().update(instance, validated_data)
        # return instance

    #         album = Album.objects.create(**validated_data)
    #         for track_data in tracks_data:
    #             Track.objects.create(album=album, **track_data)
    #         return album
    run_pools = RunPoolDetailSerializer(many=True)

    class Meta:
        model = Run
        exclude = []
        read_only_fields = ("schema",)


class ProjectDetailSerializer(ProjectSerializer):
    type = ModelRelatedField(
        model=ModelType, serializer=ModelTypeSerializer, required=False, allow_null=True
    )
    sample_type = serializers.SerializerMethodField()
    samples = SampleSerializer(many=True)

    def get_sample_type(self, obj):
        return obj.metadata.get("sample_type") if obj.metadata else None


class AdapterDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdapterDB
        exclude = []


class SubmissionTypeSerializer(serializers.ModelSerializer):
    submission_schema = JSONSchemaConverterField()

    class Meta:
        model = SubmissionType
        exclude = []


class ImporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importer
        exclude = []


class ImporterDetailSerializer(ImporterSerializer):
    submission_type = ModelRelatedField(
        model=SubmissionType, serializer=SubmissionTypeSerializer
    )
    # model_type = ModelRelatedField(model=ModelType, serializer=ModelTypeSerializer)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username", 
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
        ]
