# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

from django.db import migrations, models
from django.utils import timezone


def data_migration(apps, schema_editor):
    create_data(apps)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('talk_time', models.PositiveIntegerField(help_text='Number of seconds the agent was talking to the customer')),
                ('hold_time', models.PositiveIntegerField(help_text='Number of seconds the agent had the customer on hold')),
                ('wrap_time', models.PositiveIntegerField(help_text='Number of seconds the agent spent in after call work')),
                ('start_time', models.DateTimeField(help_text='The date and time that the call began')),
                ('agent', models.ForeignKey(to='cdr.Agent')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='team',
            field=models.ForeignKey(to='cdr.Team'),
        ),
        migrations.RunPython(data_migration)
    ]


def create_data(apps):

    CallRecord = apps.get_model('cdr', 'CallRecord')
    Agent = apps.get_model('cdr', 'Agent')
    Team = apps.get_model('cdr', 'Team')

    sales = Team.objects.create(name='Sales')
    service = Team.objects.create(name='Service')

    agents = [
        Agent.objects.create(name='Constance Clayton', team=sales),
        Agent.objects.create(name='Quamar Jarvis', team=service),
        Agent.objects.create(name='Georgia Branch', team=sales),
        Agent.objects.create(name='Beau Davenport', team=service),
        Agent.objects.create(name='Derek Holland', team=sales),
        Agent.objects.create(name='Leonard Moran', team=service),
    ]

    s1 = datetime.datetime(2015, 10, 22, 8, tzinfo=timezone.utc)
    e1 = datetime.datetime(2015, 10, 22, 21, tzinfo=timezone.utc)
    delta1 = int((e1 - s1).total_seconds())

    s2 = datetime.datetime(2014, 8, 21, 8, tzinfo=timezone.utc)
    e2 = datetime.datetime(2014, 8, 21, 21, tzinfo=timezone.utc)
    delta2 = int((e2 - s2).total_seconds())

    for x in range(1000):
        CallRecord.objects.create(
            agent=random.choice(agents),
            talk_time=random.randrange(0, 1800),
            hold_time=random.randrange(0, 600),
            wrap_time=random.randrange(5, 600),
            start_time=s1 + datetime.timedelta(
                seconds=random.randint(0, delta1)
            )
        )
        CallRecord.objects.create(
            agent=random.choice(agents),
            talk_time=random.randrange(0, 1800),
            hold_time=random.randrange(0, 600),
            wrap_time=random.randrange(5, 600),
            start_time=s2 + datetime.timedelta(
                seconds=random.randint(0, delta2)
            )
        )
