# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Constraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('enabled', models.BooleanField(default=True)),
                ('actions', models.ManyToManyField(related_name=b'constraints', to='timeslots.Action', blank=True)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConstraintSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'county',
                'verbose_name_plural': 'countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json', jsonfield.fields.JSONField(verbose_name='definition')),
                ('valid', models.DateField(verbose_name='from')),
                ('until', models.DateField(default=None, verbose_name='until', null=True, editable=False, blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('constraint', models.ForeignKey(related_name=b'definitions', verbose_name='location', to='timeslots.Constraint')),
            ],
            options={
                'ordering': ['-valid'],
                'verbose_name': 'timeslots',
                'verbose_name_plural': 'timeslots',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('reason', models.CharField(max_length=128, verbose_name='reason')),
                ('enabled', models.BooleanField(default=True)),
                ('constraint', models.ForeignKey(related_name=b'holidays', verbose_name='location', to='timeslots.Constraint')),
            ],
            options={
                'verbose_name': 'holiday',
                'verbose_name_plural': 'holiday',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='constraint',
            name='key',
            field=models.ForeignKey(related_name=b'values', to='timeslots.ConstraintSet'),
            preserve_default=True,
        ),
    ]
