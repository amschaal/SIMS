from djson.models import ModelType
from sims.id_utils import SampleNameGenerator
from sims.importers import Importer
from sims.models import Project, Sample, Pool
from django.utils import timezone

class MappedImporter(Importer):
    # def __init__(self, submission, importer):
    #     self.submission = submission
    #     self.importer = importer
    @staticmethod
    def map_data(mapping, data={}, row_data={}, array_prefix=''):
        # raise Exception(mapping.keys(), row_data, array_prefix)
        result = {}
        for k, v in mapping.items():
            if isinstance(v, dict):
                result[k] = MappedImporter.map_data(v, data, row_data, array_prefix)
            else:
                if '.' in v:
                    parts = v.split('.')
                    if parts[0] == array_prefix and len(parts) == 2:
                        result[k] = row_data.get(parts[1])
                else:
                    result[k] = data.get(v)
        return result
    def get_type(self, model, get_instance=True):
        # if self.importer.model_type:
        mapping = self.importer.config.get(model, {})
        type_id = mapping.get('type', None)
        if not get_instance:
            return type_id
        else:
            return ModelType.objects.filter(id=type_id).first() if type_id else None
        
    def get_array_data(self, model): # takes 'pool', 'sample', or 'project'
        # { "pool": { "type": "array", "source": null, "mapping": {} }, "sample": { "type": "array", "source": "samples", "mapping": { "data": { "i5": "samples[].fragment_size", "i7": "samples[].special_instructions" }, "name": "samples[].sample_name" } }, "run_type": "runtype" }
        mapping = self.importer.config.get(model)
        if not mapping or 'mapping' not in mapping:
            return []
        data = []
        # if mapping.get('type') == 'array' and mapping.get('source', None):
        if 'source' in mapping:
            source = mapping['source']
            array = self.submission.data.get(source)
            if isinstance(array, list):
                for row in array:
                    mapped = MappedImporter.map_data(mapping.get('mapping', {}), self.submission.data, row, array_prefix=source)
                    mapped['submission_data'] = row
                    data.append(mapped)
        return data
    def pool_samples(self, pools, samples):
        pool_mapping = self.importer.config.get('pool')
        pool_source = pool_mapping.get('source') # path to where pools are stored
        sample_mapping = self.importer.config.get('sample')
        sample_source = sample_mapping.get('source') # path to where samples are stored
        if not sample_source or not pool_source:
            return
        fk_field = None # this will be the sample field which is a foreign key to the pools table
        pool_field = None # the field in the pools table that is referenced
        
        # For each property in the samples table definition check if it has the "fk" property and set fields appropriately
        for id, definition in self.schema['properties'].get(sample_source, {}).get('items', {}).get('properties',{}).items():
            if definition and definition.get('fk'):
                fk = definition.get('fk')
                if fk[0] == pool_source:
                    fk_field = id
                    pool_field = fk[-1]
        
        # If FK and referenced field are found, use the original "submission_data" to pool the samples into the appropriate pool
        if fk_field and pool_field:
            for pool in pools:
                pool_samples = []
                for sample in samples:
                    if sample.submission_data.get(fk_field) and sample.submission_data.get(fk_field) == pool.submission_data.get(pool_field):
                        pool_samples.append(sample)
                pool.samples.add(*pool_samples)
                pool.locked = timezone.now()
                pool.save()
        #     pool_samples = []
        #     for sample in samples:
        #         if pool.data.get(pool_id_column) and sample.data.get(pool_id_column) == pool.data.get(pool_id_column):
        #             pool_samples.append(sample)
        #     pool.samples.add(*pool_samples)
    def get_pools(self):
        from sims.models import Pool
        pool_data = self.get_array_data('pool')
        pools = []
        model_type = self.get_type('pool')
        for fields in pool_data:
            fields['project'] = self.project
            fields['submission'] = self.submission
            fields['type'] = model_type
            pool = Pool(**fields)
            pool.unique_id = '{}_{}'.format(self.project.id, pool.name)
            pools.append(pool)
        return pools
    def get_samples(self):
        from sims.models import Sample
        sample_data = self.get_array_data('sample')
        samples = []
        model_type = self.get_type('sample')
        generator = SampleNameGenerator(self.project)
        for fields in sample_data:
            fields['project'] = self.project
            fields['submission'] = self.submission
            fields['type'] = model_type
            sample = Sample(**fields)
            sample.name = generator.next()
            sample.id = '{}_{}'.format(self.project.id, sample.name)
            samples.append(sample)
        return samples
    def get_project(self):
        project = super().get_project()
        project.metadata['types'] = { 'project': self.get_type('project', get_instance=False), 'sample': self.get_type('sample', get_instance=False), 'pool': self.get_type('pool', get_instance=False) }
        project.type = self.get_type('project')
        mapping = self.importer.config.get('project')
        if not mapping or 'mapping' not in mapping:
            return project
        project_data = MappedImporter.map_data(mapping.get('mapping', {}), self.submission.data)
        project.data = project_data.get('data', {})
        return project
    def process(self):
        self.project = self.get_project()
        samples = self.get_samples()
        pools = self.get_pools()
        # raise Exception(self.project, pools, samples)
        self.project.save()
        pools = Pool.objects.bulk_create(pools)
        samples = Sample.objects.bulk_create(samples)
        self.pool_samples(pools, samples)
        self.submission.importer = self.importer
        self.submission.processed = timezone.now()
        # self.data = self.project.submission_data
        self.submission.save()
        # libraries = Library.objects.bulk_create(libraries)
        return (self.project, pools, samples)