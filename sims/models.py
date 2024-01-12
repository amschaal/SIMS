from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from datetime import datetime
# from django.contrib.postgres.fields.jsonb import JSONField
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone

from djson.models import DjsonModel, DjsonTypeModel

class Machine(DjsonTypeModel):
    name = models.CharField(max_length=50,db_index=True)
    description = models.TextField(null=True,blank=True)
    num_lanes = models.PositiveSmallIntegerField()
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()

class Run(DjsonTypeModel):
    # type = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()

"""
This may need to be extended to:
- an individual sample where samples are not pooled (proteomics for example)
- a project, for historical metadata purposes, when in SLIMS a lane was assigned to a project
"""
class RunPool(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE,related_name='run_pools')
    index = models.PositiveSmallIntegerField()
    pool = models.ForeignKey('Pool', on_delete=models.PROTECT, null=True,blank=True,related_name='run_pools')
#     pools = models.ManyToManyField(
#         'Pool',
#         through='LanePool',
#         through_fields=('lane', 'pool'),
#     )
    description = models.TextField(null=True,blank=True,db_index=True)
    class Meta:
        unique_together = (('run','index'))
        ordering = ['run', 'index']
    def __unicode__(self):
        return '{} - {}'.format(self.run,self.index)
    def __str__(self):
        return self.__unicode__()
#     def all_libraries(self):
#         return Library.objects

class Pool(DjsonTypeModel):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    data_import = models.ForeignKey('DataImport', null=True, on_delete=models.CASCADE)
    submission_data = JSONField(default=dict)
    created = models.DateField(auto_now=True,db_index=True)
    # data = JSONField(default=dict)
    pools = models.ManyToManyField(
        'self',
        through='PoolPool',
        through_fields=('pool', 'pooled'),
        symmetrical=False,
        related_name='pooled'
    )
#     pooled = models.ManyToManyField(
#         'self',
#         through='PoolPool',
#         through_fields=('pooled', 'pool'),
#         symmetrical=False
#     )
    samples = models.ManyToManyField(
        'Sample',
        through='SamplePool',
        through_fields=('pool', 'sample'),
        related_name='pools'
    )
#     libraries = models.ManyToManyField(Library,related_name='pools')
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()
#     def get_absolute_url(self):
#         return reverse('pool', args=[str(self.id)])
    def get_barcode_duplicates(self):
        barcodes = self.get_library_barcodes()
        duplicates = {barcode:libraries for barcode,libraries in barcodes.iteritems() if len(libraries) > 1}
        return duplicates if len(duplicates) > 0 else None
    def get_library_barcodes(self):
        barcodes = {}
        for l in self.samples.select_related('adapter').filter(adapter__isnull=False):
            if not barcodes.has_key(l.adapter.barcode):
                barcodes[l.adapter.barcode] = []
            barcodes[l.adapter.barcode].append(l.name)
        return barcodes

#     pools = models.ManyToManyField(
#         'Pool',
#         through='LanePool',
#         through_fields=('lane', 'pool'),
#     )

class PoolLibrary(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.PROTECT)
    class Meta:
        unique_together = (('pool','library'))

class SamplePool(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    class Meta:
        unique_together = (('pool','sample'))

# Maybe this is excessive.  Instead when putting pools together, samples could just be joined into a standard Pool.
class PoolPool(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='pooled_intermediate')
    pooled = models.ForeignKey(Pool, on_delete=models.PROTECT, related_name='pools_intermediate')
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)], null=True, blank=True)
    class Meta:
        unique_together = (('pool','pooled'))



#===============================================================================
# Project contains minimal subset of information from sample submission system.
# Data may be imported and updated from submission system.
# This helps create local DB FKs as well as make submissions quickly searchable instead of using API.
#===============================================================================
class Project(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    submission_id = models.CharField(max_length=50, unique=True, editable=False)
#     status = models.CharField(max_length=50, null=True)#models.ForeignKey(SubmissionStatus,null=True,on_delete=models.SET_NULL)
#     locked = models.BooleanField(default=False)
#     cancelled = models.DateTimeField(null=True, blank=True)
#     completed = models.DateTimeField(null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
#     confirmed = models.DateTimeField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20)
    pi_first_name = models.CharField(max_length=50)
    pi_last_name = models.CharField(max_length=50)
    pi_email = models.EmailField(max_length=75)
    pi_phone = models.CharField(max_length=20)
    institute = models.CharField(max_length=75)
#     payment_type = models.CharField(max_length=50,choices=PAYMENT_CHOICES)
#     payment_info = models.CharField(max_length=250,null=True,blank=True)
#     type = models.ForeignKey(SubmissionType,related_name="submissions", on_delete=models.PROTECT)
    type = JSONField()
    submission_schema = JSONField(null=True,blank=True)
    sample_schema = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    sample_data = JSONField(null=True,blank=True)
    biocore = models.BooleanField(default=False)
#     participants = models.ManyToManyField(User,blank=True)
    data = JSONField(default=dict)
    comments = models.TextField(null=True, blank=True)
    # plugin_data = JSONField(default=dict)s = models.TextField(null=True,blank=True)

class DataImport(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    imported = models.DateTimeField(null=True)
    data = models.JSONField(default=dict)
    def process(self):
        if not self.imported:
            from sims.transform import create_project_samples, pool_samples
            pools, samples = create_project_samples(self.project, self)
            pools = Pool.objects.bulk_create(pools)
            samples = Sample.objects.bulk_create(samples)
            pool_samples(self.project, pools, samples)
            self.imported = timezone.now()
            self.data = self.project.submission_data
            self.save()
            # libraries = Library.objects.bulk_create(libraries)
            return (pools, samples)

class Sample(DjsonTypeModel):
    TYPE_LIBRARY = 'LIBRARY'
    id = models.CharField(max_length=50,primary_key=True)
    physical_type = models.CharField(max_length=25, null=True)
    sample = models.ForeignKey('self', related_name='samples', null=True, on_delete=models.RESTRICT) #derived from
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="samples",null=True,blank=True)
    name = models.CharField(max_length=50,db_index=True)
    imported = models.DateTimeField(auto_now=True,db_index=True)
    data_import = models.ForeignKey(DataImport, null=True, on_delete=models.CASCADE)
    # data = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    # fields below are for library only
    adapter = models.ForeignKey('Adapter', on_delete=models.PROTECT,null=True,blank=True,related_name='samples')
    barcodes = JSONField(default=dict, null=True)
#     received = models.DateField(null=True,blank=True,db_index=True)
    def __unicode__(self):
        return self.id
    def __str__(self):
        return self.id
#     def get_absolute_url(self):
#         return reverse('sample', args=[str(self.id)])
#     def directory(self,full=True):
#         return call_directory_function('get_sample_directory',self,full=full)
    class Meta:
        unique_together = (('id','project'),)
#     @transaction.atomic
#     def save(self, *args, **kwargs):
#         if not self.id:
# #             if not self.id and self.project:
# #             last = Sample.objects.filter(project=self.project,id__regex=r'^[A-Z]\d{2}').last()
#             id = generate_id(self.project)
#             self.id = id
#         super(Sample, self).save(*args, **kwargs)

class AdapterDB(models.Model):
    id = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

class Adapter(models.Model):
    db = models.ForeignKey(AdapterDB, on_delete=models.CASCADE, related_name="adapters")
    name = models.CharField(max_length=100)
    barcodes = JSONField(default=dict)
    class Meta:
        unique_together = (('db','name'))
    def __unicode__(self):
        return '{} ({})'.format(self.db, self.name)
    def __str__(self):
        return '{} ({})'.format(self.db, self.name)

# Maybe this goes away, and a library becomes just a type of sample with adapter/barcodes
class Library(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,related_name='libraries')
    adapter = models.ForeignKey(Adapter, on_delete=models.PROTECT,null=True,blank=True,related_name='libraries')
    barcodes = JSONField(default=dict)
#     barcode = models.CharField(max_length=100, null=True, blank=True) #this should be updated if adapter changed
    description = models.TextField(null=True,blank=True,db_index=True)
    def get_group(self):
        try:
            return self.sample.project.group
        except:
            return None
    def __unicode__(self):
        return self.id
    def name(self):
        return self.id
    
@receiver(pre_save,sender=Library)
def set_barcodes(sender,instance,**kwargs):
#     if instance.adapter and not instance.barcodes:
    instance.barcodes = instance.adapter.barcodes
    if not instance.id:
        instance.id = 'L_'+instance.sample.id

@receiver(pre_save,sender=Run)
def set_run_name(sender,instance,**kwargs):
    if instance.name and instance.id:
        return
    if not instance.name:
        t = instance.created or datetime.now()
        instance.name = '%s: %s' % (instance.machine.name, t.strftime('%Y-%m-%d'))

@receiver(post_save,sender=Run)
def create_run(sender,instance,created,**kwargs):
    if created:
        for i in range(1,instance.machine.num_lanes+1):
            RunPool.objects.create(run=instance, index=i)
