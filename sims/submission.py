from django.utils import timezone
import urllib.request, json
from django.conf import settings
from sims.models import Project, Sample
from django.conf.urls.static import static

class Submission(object):
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.internal_id = data['internal_id']
        self.submitted = data['submitted']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pi_first_name = data['pi_first_name']
        self.pi_last_name = data['pi_last_name']
        self.pi_email = data['pi_email']
        self.institute = data['institute']
        self.type = data['type']
        self.submission_schema = data['submission_schema']
        # self.sample_schema = data['sample_schema']
        self.submission_data = data['submission_data']
        # self.sample_data = data['sample_data']
        self.biocore = data['biocore']
        self.data = data['data']
        self.comments = data['comments']
    def create_project(self):
        from sims.models import Project
        if Project.objects.filter(submission_id=self.id).first():
            raise Exception('Submission "{0}" has already been imported.'.format(self.id))
        project = Project.objects.create(id=self.internal_id or self.id, 
                                         submission_id=self.id, 
                                         submitted=self.submitted,
                                         created=timezone.now(),
                                         first_name=self.first_name,
                                         last_name=self.last_name,
                                         email=self.email,
                                         pi_first_name = self.pi_first_name,
                                         pi_last_name = self.pi_last_name,
                                         pi_email=self.pi_email,
                                         institute=self.institute,
                                         type=self.type,
                                         submission_schema=self.submission_schema,
                                        #  sample_schema=self.sample_schema,
                                         submission_data=self.submission_data,
                                        #  sample_data=self.sample_data,
                                        #  biocore=self.biocore,
                                         data=self.data,
                                         comments=self.comments
                                         )
#         Sample.objects.bulk_create([Sample(project=project,id='{}_{}'.format(project.id,s.get('sample_name')),name=s.get('sample_name'),data=s) for s in self.sample_data])
        self.update_samples(project, import_only=True)
        return project
    def update_samples(self, project, import_only=True):
        # sample_ids = list(project.samples.all().values_list('id', flat=True))
        # new_samples = [s for s in self.sample_data if self.get_sample_id(project, s) not in sample_ids]
        new_samples = []
        return Sample.objects.bulk_create([Sample(project=project,id=self.get_sample_id(project, s),name=s.get('sample_name'),data=s) for s in new_samples])
    @staticmethod
    def get_sample_id(project, sample):
        return '{}_{}'.format(project.id,sample.get('sample_name'))
    @staticmethod
    def get_submission(id_or_url):
        if '://' in id_or_url:
            URL = id_or_url.replace('/submissions/', '/server/api/submissions/')
        else:
            URL = settings.SUBMISSION_SYSTEM_URLS['api']['submission'].format(id=id)
        print('URL', URL)
        with urllib.request.urlopen(URL) as url:
            data = url if isinstance(url, str) else url.read().decode('utf-8')
            data = json.loads(data)#url.read().decode()
            print(data)
            return Submission(data)
