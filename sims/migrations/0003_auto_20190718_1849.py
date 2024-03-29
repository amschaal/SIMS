# Generated by Django 2.2.3 on 2019-07-18 18:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sims', '0002_auto_20190717_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poolpool',
            name='percentage',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='runpool',
            name='pool',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='run_pools', to='sims.Pool'),
        ),
    ]
