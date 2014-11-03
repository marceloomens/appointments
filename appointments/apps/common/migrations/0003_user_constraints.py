# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeslots', '0003_auto_20141102_0853'),
        ('common', '0002_report_last_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='constraints',
            field=models.ManyToManyField(related_name='+', to='timeslots.Constraint'),
            preserve_default=True,
        ),
    ]
