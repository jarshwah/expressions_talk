try:
    from django.db.models.expressions import *
    from django.db.models.functions import *
    from django.db.models.lookups import *
except ImportError:
    pass

from .models import Agent, CallRecord


def total_talktime():
    """
    A simple aggregation.
    """
    return CallRecord.objects.aggregate(sum_talk_time=Sum('talk_time'))


def conditional_annotation():
    """
    Demonstrates an aggregation that has a conditional
    filter.
    """
    from django.db.models import Case, Count, When

    return Agent.objects.annotate(
        count_2014=Count(Case(When(callrecord__start_time__year=2014, then=1))),
        count_2015=Count(Case(When(callrecord__start_time__year=2015, then=1))),
    )


def date_based_aggregate():
    from django.db.models import Count
    from .functions import JustTheDate

    return CallRecord.objects.annotate(
        start_date=JustTheDate('start_time')
    ).values('start_date').annotate(call_count=Count('pk'))
