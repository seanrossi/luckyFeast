# Generated by Django 2.0.7 on 2018-07-25 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0004_auto_20180721_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rsvp_count',
            field=models.IntegerField(default=0),
        ),
    ]
