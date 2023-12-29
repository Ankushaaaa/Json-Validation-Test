import json
from typing import Dict, List, Optional, Union


class JsonValidator:
    def __init__(self):
        pass

    def _validate_required_fields(self, json_data, required_fields):
        for field in required_fields:
            if field not in json_data:
                return False
        return True

    def _validate_at_least_one_of(self, json_data, fields):
        present_fields = [field for field in fields if field in json_data]
        return len(present_fields) >= 1

    def _validate_either_one_of(self, json_data, field1, field2):
        return (field1 in json_data and field2 not in json_data) or \
               (field1 not in json_data and field2 in json_data)

    def _validate_mutually_exclusive(self, json_data, field1, field2):
        return (field1 in json_data and field2 not in json_data) or \
               (field1 not in json_data and field2 in json_data) or \
               (field1 not in json_data and field2 not in json_data)

    def _validate_field_values(self, json_data, field, allowed_values):
        return field in json_data and json_data[field] in allowed_values

    def validate_schema(self, json_file, schema_file):
        with open(json_file, 'r') as json_file:
            json_data = json.load(json_file)

        with open(schema_file, 'r') as schema_file:
            schema = json.load(schema_file)

        # Validate Required Fields
        if 'required_fields' in schema:
            if not self._validate_required_fields(json_data, schema['required_fields']):
                return False

        # Validate At Least One Of
        if 'at_least_one_of' in schema:
            if not self._validate_at_least_one_of(json_data, schema['at_least_one_of']):
                return False

        # Validate Either One Of
        if 'either_one_of' in schema:
            field1, field2 = schema['either_one_of']
            if not self._validate_either_one_of(json_data, field1, field2):
                return False

        # Validate Mutually Exclusive
        if 'mutually_exclusive' in schema:
            field1, field2 = schema['mutually_exclusive']
            if not self._validate_mutually_exclusive(json_data, field1, field2):
                return False

        # Validate Field Values
        if 'field_values' in schema:
            for field, allowed_values in schema['field_values'].items():
                if not self._validate_field_values(json_data, field, allowed_values):
                    return False

        return True


# Example Usage
validator = JsonValidator()
result = validator.validate_schema('data.json', 'schema.json')
print(result)
