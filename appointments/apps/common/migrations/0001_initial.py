# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('timeslots', '0004_auto_20141002_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=64, null=True, blank=True)),
                ('last_name', models.CharField(max_length=64, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(default=b'PE', max_length=2, choices=[(b'PE', b'pending'), (b'CO', b'confirmed'), (b'CA', b'cancelled')])),
                ('first_name', models.CharField(max_length=64, null=True, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=64, null=True, verbose_name='last name', blank=True)),
                ('nationality', models.CharField(max_length=32, null=True, verbose_name='nationality', blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name='sex', choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('identity_number', models.CharField(max_length=64, null=True, verbose_name='identity number', blank=True)),
                ('document_number', models.CharField(max_length=64, null=True, verbose_name='document number', blank=True)),
                ('phone_number', models.CharField(max_length=16, null=True, verbose_name='phone number', blank=True)),
                ('mobile_number', models.CharField(max_length=16, null=True, verbose_name='mobile number', blank=True)),
                ('comment', models.TextField(null=True, verbose_name='comment', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('action', models.ForeignKey(related_name=b'+', verbose_name='action', to='timeslots.Action')),
                ('constraint', models.ForeignKey(related_name=b'+', verbose_name='location', to='timeslots.Constraint')),
                ('user', models.ForeignKey(related_name=b'appointments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'appointment',
                'verbose_name_plural': 'appointments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(default=b'DA', max_length=2, choices=[(b'DA', b'daily')])),
                ('last_sent', models.DateTimeField(default=None, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('constraint', models.ForeignKey(related_name=b'+', verbose_name='location', to='timeslots.Constraint')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
