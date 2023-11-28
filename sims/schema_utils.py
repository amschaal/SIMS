def convert_to_jsonschema(coreomics_schema):
    import copy
    schema = copy.deepcopy(coreomics_schema)
    # Make changes to schema
    for prop in schema['properties'].keys():
        if 'table' == schema['properties'].get('prop',{}).get('type', '').lower():
            schema['properties'][prop]['type'] = 'array'
            schema['properties'][prop]['items'] = schema['properties'][prop].pop('schema')
            schema['properties'][prop]['items']['type'] = 'object'
    return coreomics_schema

def transform_errors(jsonschema_errors):
    errors = {}
    # build errors in format for coreomics
    return errors