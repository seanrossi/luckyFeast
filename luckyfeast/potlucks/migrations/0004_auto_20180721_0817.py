# Generated by Django 2.0.7 on 2018-07-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0003_event_event_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest_instance',
            name='rsvp_status',
            field=models.IntegerField(choices=[(1, 'Undecided'), (2, 'Yes'), (3, 'No')], default=1),
        ),
    ]
