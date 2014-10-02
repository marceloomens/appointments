# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_remove_report_last_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='last_sent',
            field=models.DateTimeField(default=None, null=True),
            preserve_default=True,
        ),
    ]
