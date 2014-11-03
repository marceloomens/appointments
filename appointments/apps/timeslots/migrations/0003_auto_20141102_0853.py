# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeslots', '0002_constraint_timezone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constraintset',
            options={'verbose_name': 'country', 'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='holiday',
            options={'verbose_name': 'holiday', 'verbose_name_plural': 'holidays'},
        ),
    ]
