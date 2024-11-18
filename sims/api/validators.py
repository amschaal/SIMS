from rest_framework import serializers
import re

class BarcodeValidator:
    requires_context = True
    barcode_re = r'^[ATGCN]*$'
    def __init__(self):
        pass
    def validate_barcode(self, field, barcode):
        if barcode and not re.match(self.barcode_re, barcode):
            self.errors[field] = 'Barcode "{}" does not match expression: {}'.format(barcode, self.barcode_re)
    def __call__(self, value, serializer_field):
        self.errors = {}
        if not value:
            return
        self.serializer_field = serializer_field
        self.validate_barcode('i5', value.get('i5'))
        self.validate_barcode('i7', value.get('i7'))
        if self.errors:
            raise serializers.ValidationError(self.errors)