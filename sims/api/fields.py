from rest_framework.fields import JSONField

from sims.schema_utils import convert_to_jsonschema

# Helper for temporarily trying different jsonschema format without changing underlying value
class JSONSchemaConverterField(JSONField):
    def to_representation(self, value):
        value = super().to_representation(value)
        return convert_to_jsonschema(value)