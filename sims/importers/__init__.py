from django.utils import timezone

from sims.schema_utils import convert_to_jsonschema

class Importer(object):
    def __init__(self, submission, importer, config=None):
        self.submission = submission
        self.importer = importer
        self.schema = convert_to_jsonschema(submission.schema)
    def delete_imported(self):
        """
        Cleanup any resources created before deleting import
        """
        from sims.models import Pool, Sample, Project
        Sample.objects.filter(submission=self.submission).delete()
        Pool.objects.filter(submission=self.submission).delete()
        Project.objects.filter(submission=self.submission).delete()
    def get_project(self):
        from sims.models import Project
        submission = self.submission
        project = Project(
            id=submission.submission_id or submission.id,
            type=self.importer.model_type,
            # submission_id=submission.submission_id,
            first_name=submission.first_name,
            last_name=submission.last_name,
            email=submission.email,
            phone=submission.phone,
            pi_first_name=submission.pi_first_name,
            pi_last_name=submission.pi_last_name,
            pi_email=submission.pi_email,
            pi_phone=submission.pi_phone,
            institute=submission.institute,
            comments=submission.comments,
            submission_data=submission.data,
            submission=submission,
            submitted = submission.submitted,
            created = timezone.now()
            )
        return project
    def process(self):
        raise NotImplementedError