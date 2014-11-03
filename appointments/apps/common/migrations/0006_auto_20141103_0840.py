# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20141103_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='comment',
            field=models.TextField(default=b'', verbose_name='comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='document_number',
            field=models.CharField(default=b'', max_length=64, verbose_name='document number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(default=b'', max_length=64, verbose_name='first name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='identity_number',
            field=models.CharField(default=b'', max_length=64, verbose_name='identity number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='last_name',
            field=models.CharField(default=b'', max_length=64, verbose_name='last name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='mobile_number',
            field=models.CharField(default=b'', max_length=16, verbose_name='mobile number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='nationality',
            field=models.CharField(default=b'', max_length=32, verbose_name='nationality', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='phone_number',
            field=models.CharField(default=b'', max_length=16, verbose_name='phone number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='sex',
            field=models.CharField(default=b'', max_length=1, verbose_name='sex', blank=True, choices=[(b'M', 'Male'), (b'F', 'Female')]),
            preserve_default=True,
        ),
    ]
