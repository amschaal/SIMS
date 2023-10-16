from .models import Pool, Sample, Library, Project
# Maybe use this: https://github.com/kennknowles/python-jsonpath-rw

pool_field_map = {
        'row': 'pools',
        'fields': {
            'name': 'pool_name',
            'description': None
        },
        'data': '*' # * indicates all fields should be kept in data, None -> none, ['field1','field2'] for a list of fields to retain
    }

sample_field_map = {
    'row': 'samples',
    'fields': {
        'name': 'sample_name'
    },
    'data': '*' # * indicates all fields should be kept in data, None -> none, ['field1','field2'] for a list of fields to retain
}

def get_pools(project, field_map):
    schema = project.submission_schema
    data = project.submission_data
    pools = []
    for row in data[field_map['row']]:
        fields = {key: row[val] for key, val in field_map['fields'].items()}
        fields['data'] = row
        pools.append(Pool(**fields))
    return pools

def get_samples(project, field_map=sample_field_map):
    # need to handle pools
    schema = project.submission_schema
    data = project.submission_data
    samples = []
    for row in data[field_map['row']]:
        fields = {key: row[val] for key, val in field_map['fields'].items()}
        fields['data'] = row
        fields['project'] = project
        sample = Sample(**fields)
        sample.id = '{}_{}'.format(project.id,sample.name)
        samples.append(sample)
    return samples


"""
class Pool(models.Model):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    created = models.DateField(auto_now=True,db_index=True)

class Sample(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    type = models.CharField(max_length=25)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="samples",null=True,blank=True)
    name = models.CharField(max_length=50,db_index=True)
    imported = models.DateTimeField(auto_now=True,db_index=True)
#     received = models.DateField(null=True,blank=True,db_index=True)
    data = JSONField(null=True,blank=True)

def update_samples(self, project, import_only=True):
        # sample_ids = list(project.samples.all().values_list('id', flat=True))
        # new_samples = [s for s in self.sample_data if self.get_sample_id(project, s) not in sample_ids]
        new_samples = []
        return Sample.objects.bulk_create([Sample(project=project,id=self.get_sample_id(project, s),name=s.get('sample_name'),data=s) for s in new_samples])
    @staticmethod
    def get_sample_id(project, sample):
        return '{}_{}'.format(project.id,sample.get('sample_name'))


Sample:
    type: 'library'
    id: libraries.library_name
    pool: Pool.id
    data: 

Pool:
    id: pools.pool_name
    volume: pools.volume
    ...
    data: pools[['concentration', ...]]

Sample:
    type: 'protein'
    id:
    foo:
    bar:
    data:

"""

"""

{
	"submission_data": {
		"i5": null,
		"i7": "NextSeq",
		"demux": "Yes",
		"lanes": "1",
		"notes": null,
		"pools": [
			{
				"phix": "1% (default)",
				"buffer": "EB",
				"libkit": "lexigen",
				"volume": 20,
				"libtype": "TagSeq",
				"organism": "lettuce",
				"flow_cell": "1",
				"pool_name": "TAGSEQ_91321",
				"bioanalyzer": "Yes",
				"concentration": 6.24,
				"limited_input": "No",
				"quantification": "Qubit"
			}
		],
		"runtype": "HiSeq SE100",
		"index_len": "6bp",
		"libraries": [
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7001",
				"library_name": "01"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7002",
				"library_name": "02"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7003",
				"library_name": "03"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7004",
				"library_name": "04"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7005",
				"library_name": "05"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7006",
				"library_name": "06"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7007",
				"library_name": "07"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7008",
				"library_name": "08"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7009",
				"library_name": "09"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7010",
				"library_name": "10"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7011",
				"library_name": "11"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7012",
				"library_name": "12"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7013",
				"library_name": "13"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7014",
				"library_name": "14"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7015",
				"library_name": "15"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7016",
				"library_name": "16"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7017",
				"library_name": "17"
			},
			{
				"pool_name": "TAGSEQ_91321",
				"index_name": "7018",
				"library_name": "18"
			}
		],
		"index_desc": "Single",
		"run_directory": null,
		"custom_primers": null
	}
}
"""