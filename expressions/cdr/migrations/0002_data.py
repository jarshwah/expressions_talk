# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from ..data import create_initial_data


class Migration(migrations.Migration):

    dependencies = [
        ('cdr', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data)
    ]
