# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20141102_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='constraints',
            field=models.ManyToManyField(related_name='+', to='timeslots.Constraint', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
