


class Importer(object):
    def __init__(self, submission, importer):
        self.submission = submission
        self.importer = importer
    def get_project(self):
        from sims.models import Project
        submission = self.submission
        project = Project(
            id=submission.submission_id or submission.id,
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
            submission=submission
            )
        return project
    def process(self):
        raise NotImplementedError