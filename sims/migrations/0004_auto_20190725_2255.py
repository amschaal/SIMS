# Generated by Django 2.2.3 on 2019-07-25 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sims', '0003_auto_20190718_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='email',
            field=models.EmailField(default='fake', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='phone',
            field=models.CharField(default='fake', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='pi_email',
            field=models.EmailField(default='fake', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='pi_phone',
            field=models.CharField(default='fake', max_length=20),
            preserve_default=False,
        ),
    ]
