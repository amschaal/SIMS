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
    def __str__(self):
        return self.__unicode__()

class Run(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()

class RunPool(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE,related_name='run_pools')
    index = models.PositiveSmallIntegerField()
    pool = models.ForeignKey('Pool', on_delete=models.PROTECT, null=True,blank=True)
#     pools = models.ManyToManyField(
#         'Pool',
#         through='LanePool',
#         through_fields=('lane', 'pool'),
#     )
    description = models.TextField(null=True,blank=True,db_index=True)
    class Meta:
        unique_together = (('run','index'))
    def __unicode__(self):
        return '{} - {}'.format(self.run,self.index)
    def __str__(self):
        return self.__unicode__()

class Pool(models.Model):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    created = models.DateField(auto_now=True,db_index=True)
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
    libraries = models.ManyToManyField(
        'Library',
        through='PoolLibrary',
        through_fields=('pool', 'library'),
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
        for l in self.libraries.select_related('adapter').filter(adapter__isnull=False):
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

class PoolPool(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='pooled_intermediate')
    pooled = models.ForeignKey(Pool, on_delete=models.PROTECT, related_name='pools_intermediate')
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
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
    type = JSONField()
    submission_schema = JSONField(null=True,blank=True)
    sample_schema = JSONField(null=True,blank=True)
    submission_data = JSONField(default=dict)
    sample_data = JSONField(null=True,blank=True)
    biocore = models.BooleanField(default=False)
#     participants = models.ManyToManyField(User,blank=True)
    data = JSONField(default=dict)
    comments = models.TextField(null=True, blank=True)

class Sample(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="samples",null=True,blank=True)
#     name = models.CharField(max_length=100,db_index=True)
    imported = models.DateTimeField(auto_now=True,db_index=True)
#     received = models.DateField(null=True,blank=True,db_index=True)
    data = JSONField(null=True,blank=True)
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

class Adapter(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return '{} ({})'.format(self.name,self.barcode)
    def __str__(self):
        return '{} ({})'.format(self.name,self.barcode)

class Library(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
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
        return self.id
    def name(self):
        return self.id
    
@receiver(pre_save,sender=Library)
def set_barcode(sender,instance,**kwargs):
    if instance.adapter and not instance.barcode:
        instance.barcode = instance.adapter.barcode
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
