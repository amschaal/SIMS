import urllib.request, json
from django.conf import settings
from sims.models import Project, Sample

class Submission(object):
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.internal_id = data['internal_id']
        self.submitted = data['submitted']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.pi_first_name = data['pi_first_name']
        self.pi_last_name = data['pi_last_name']
        self.institute = data['institute']
        self.type = data['type']
        self.submission_schema = data['submission_schema']
        self.sample_schema = data['sample_schema']
        self.submission_data = data['submission_data']
        self.sample_data = data['sample_data']
        self.biocore = data['biocore']
        self.data = data['data']
        self.comments = data['comments']
    def create_project(self):
        print(self.comments)
        project = Project.objects.create(id=self.internal_id, 
                                         submission_id=self.id, 
                                         submitted=self.submitted,
                                         first_name=self.first_name,
                                         last_name=self.last_name,
                                         institute=self.institute,
                                         type=self.type,
                                         submission_schema=self.submission_schema,
                                         sample_schema=self.sample_schema,
                                         submission_data=self.submission_data,
                                         sample_data=self.sample_data,
                                         biocore=self.biocore,
                                         data=self.data,
                                         comments=self.comments
                                         )
        Sample.objects.bulk_create([Sample(project=project,id=s.get('sample_name'),data=s) for s in self.sample_data])
        return project
    @staticmethod
    def get_submission(id):
        URL = settings.SUBMISSION_SYSTEM_URLS['submission'].format(id=id)
        with urllib.request.urlopen(URL) as url:
            data = json.load(url)#url.read().decode()
            return Submission(data)
