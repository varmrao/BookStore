# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-02 20:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstr', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookbuytrans',
            name='date',
        ),
    ]
