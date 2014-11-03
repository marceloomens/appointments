# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeslots', '0003_auto_20141102_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='reason',
            field=models.CharField(default=b'', max_length=128, verbose_name='reason', blank=True),
            preserve_default=True,
        ),
    ]
