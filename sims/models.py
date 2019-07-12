from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from datetime import datetime
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Machine(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    description = models.TextField(null=True,blank=True)
    num_lanes = models.SmallIntegerField()
    def __unicode__(self):
        return self.name

class Run(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    description = models.TextField(null=True,blank=True)

class Lane(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE,related_name='lanes')
    index = models.PositiveSmallIntegerField()
#     pool = models.ForeignKey('Pool',null=True,blank=True)
    pools = models.ManyToManyField(
        'Pool',
        through='LanePool',
        through_fields=('lane', 'pool'),
    )
    description = models.TextField(null=True,blank=True,db_index=True)
    class Meta:
        unique_together = (('run','index'))

class LanePool(models.Model):
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name='lane_pools')
    pool = models.ForeignKey('Pool', on_delete=models.PROTECT)
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

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
            Lane.objects.create(run=instance, index=i)

#===============================================================================
# Submission contains minimal subset of information from sample submission system.
# Data may be imported and updated from submission system.
# This helps create local DB FKs as well as make submissions quickly searchable instead of using API.
#===============================================================================
class Submission(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    internal_id = models.CharField(max_length=25)
#     status = models.CharField(max_length=50, null=True)#models.ForeignKey(SubmissionStatus,null=True,on_delete=models.SET_NULL)
#     locked = models.BooleanField(default=False)
#     cancelled = models.DateTimeField(null=True, blank=True)
#     completed = models.DateTimeField(null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
#     confirmed = models.DateTimeField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=75)
#     phone = models.CharField(max_length=20)
    pi_first_name = models.CharField(max_length=50)
    pi_last_name = models.CharField(max_length=50)
#     pi_email = models.EmailField(max_length=75)
#     pi_phone = models.CharField(max_length=20)
    institute = models.CharField(max_length=75)
#     payment_type = models.CharField(max_length=50,choices=PAYMENT_CHOICES)
#     payment_info = models.CharField(max_length=250,null=True,blank=True)
#     type = models.ForeignKey(SubmissionType,related_name="submissions", on_delete=models.PROTECT)
    type = models.CharField(max_length=50)
    submission_schema = JSONField(null=True,blank=True)
    sample_schema = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    sample_data = JSONField(null=True,blank=True)
    biocore = models.BooleanField(default=False)
#     participants = models.ManyToManyField(User,blank=True)
    data = JSONField(default=dict)
    comments = models.TextField(null=True, blank=True)

class Sample(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="samples",null=True,blank=True)
    sample_id = models.CharField(max_length=60,unique=True,null=True,blank=True,db_index=True)
    name = models.CharField(max_length=100,db_index=True)
    imported = models.DateTimeField(auto_now=True,db_index=True)
#     received = models.DateField(null=True,blank=True,db_index=True)
    data = JSONField(null=True,blank=True)
    def __unicode__(self):
        return self.sample_id
#     def get_absolute_url(self):
#         return reverse('sample', args=[str(self.id)])
#     def directory(self,full=True):
#         return call_directory_function('get_sample_directory',self,full=full)
    class Meta:
        unique_together = (('sample_id','submission'),('name','submission'),)
#     @transaction.atomic
#     def save(self, *args, **kwargs):
#         if not self.id:
# #             if not self.sample_id and self.project:
# #             last = Sample.objects.filter(project=self.project,sample_id__regex=r'^[A-Z]\d{2}').last()
#             sample_id = generate_sample_id(self.project)
#             self.sample_id = sample_id
#         super(Sample, self).save(*args, **kwargs)

class Adapter(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)

class Library(models.Model):
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    name = models.CharField(max_length=100,null=True,blank=True,db_index=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,related_name='libraries')
    adapter = models.ForeignKey(Adapter, on_delete=models.PROTECT,null=True,blank=True,related_name='libraries')
    barcode = models.CharField(max_length=100, null=True, blank=True) #this should be updated if adapter changed
    description = models.TextField(null=True,blank=True,db_index=True)
    def get_group(self):
        try:
            return self.sample.project.group
        except:
            return None
    def __unicode__(self):
        return self.name

class Pool(models.Model):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    created = models.DateField(auto_now=True,db_index=True)
    libraries = models.ManyToManyField(Library,related_name='pools')
    library_data = JSONField(null=True,blank=True,default={})
    def __unicode__(self):
        return self.name
#     def get_absolute_url(self):
#         return reverse('pool', args=[str(self.id)])
    def get_barcode_duplicates(self):
        barcodes = self.get_library_barcodes()
        duplicates = {barcode:libraries for barcode,libraries in barcodes.iteritems() if len(libraries) > 1}
        return duplicates if len(duplicates) > 0 else None
    def get_library_barcodes(self):
        barcodes = {}
        for l in self.libraries.select_related('adapter').filter(adapter__isnull=False):
            if not barcodes.has_key(l.adapter.barcode):
                barcodes[l.adapter.barcode] = []
            barcodes[l.adapter.barcode].append(l.name)
        return barcodes


