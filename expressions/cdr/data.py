import datetime
import random
from django.utils import timezone


def create_initial_data(apps, schema_editor):
    """
    Remember to add the following to a migration!

    ```
    from ..data import create_initial_data
    migrations.RunPython(create_initial_data)
    ```
    """
    CallRecord = apps.get_model('cdr', 'CallRecord')
    Agent = apps.get_model('cdr', 'Agent')
    Team = apps.get_model('cdr', 'Team')

    sales = Team.objects.create(name='Sales')
    service = Team.objects.create(name='Service')

    agents = [
        Agent.objects.create(name='Constance Clayton'),
        Agent.objects.create(name='Quamar Jarvis', team=service),
        Agent.objects.create(name='Georgia Branch', team=sales),
        Agent.objects.create(name='Beau Davenport', team=service),
        Agent.objects.create(name='Derek Holland', team=sales),
        Agent.objects.create(name='Leonard Moran'),
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
