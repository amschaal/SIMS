from sims.models import Project

class SampleNameGenerator(object):
    def __init__(self, project: Project, zfill=4, starting=1):
        self.project = project
        self.zfill = zfill
        self.current = starting - 1
        self.sample_names = set(self.project.samples.values_list("name", flat=True).order_by("name"))
    def next(self):
        self.current += 1
        name = str(self.current).zfill(self.zfill)
        while name in self.sample_names:
            self.current += 1
            name = str(self.current).zfill(self.zfill)
        return name