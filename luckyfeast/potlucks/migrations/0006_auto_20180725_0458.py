# Generated by Django 2.0.7 on 2018-07-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0005_event_rsvp_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='event',
            name='apt',
        ),
        migrations.RemoveField(
            model_name='event',
            name='city',
        ),
        migrations.RemoveField(
            model_name='event',
            name='state',
        ),
        migrations.RemoveField(
            model_name='event',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='', max_length=50),
        ),
    ]
