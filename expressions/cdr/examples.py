from django.db.models import Avg, Case, Count, Sum, When
from django.db.models.expressions import *  # NOQA
from django.db.models.functions import *    # NOQA
from django.db.models.lookups import *      # NOQA

from .functions import Date
from .models import Agent, CallRecord


def include_team_expressions():
    """
    Append a column to the result.
    """
    return (
        CallRecord.objects
            .annotate(team=Coalesce(
                'agent__team__name',
                Value('No Team')
            ))
    )


def include_team_extra():
    """
    Append a column to the result.
    """
    sql = "COALESCE(cdr_team.name, 'No Team')"
    return (
        CallRecord.objects
            .select_related('agent__team')
            .extra(select={
                'team':
                sql})
    )


def aht_per_team():
    """
    Calculate a combined aggregate across a custom
    dimension.
    """
    return (
        CallRecord.objects.annotate(
            team=Coalesce(
                'agent__team__name',
                Value('No Team')
        ))
        .values('team')
        .annotate(
            aht=Avg(
                F('talk_time') +
                F('hold_time') +
                F('wrap_time')
        ))
        .order_by('team')
    )


def conditional_annotation():
    """
    Demonstrates an aggregation that has a conditional
    filter.
    """

    return (
        Agent.objects
            .annotate(
            count_2014=Count(
                Case(When(
                    callrecord__start_time__year=2014,
                    then=1))),
            count_2015=Count(
                Case(When(
                    callrecord__start_time__year=2015,
                    then=1))),
        ))


def date_based_aggregate():
    """
    Aggregate based on the date, stripping time
    from the datetime.
    """
    return (
        CallRecord.objects
            .annotate(start_date=Date('start_time'))
            .values('start_date')
            .annotate(call_count=Count('pk'))
    )


def relabeled_example():
    hold = F('hold_time')
    subq = CallRecord.objects.filter(
        wrap_time__gt=hold)
    qs = CallRecord.objects.filter(
        talk_time__gt=hold,
        id__in=subq)


def the_future():
    """
    This code doesn't actually work, but highlights
    what could potentially exist as syntax in the
    future.
    """
    CallRecord.objects.order_by(
        F('talk_time') - F('hold_time'))

    class Date(Func):
        pass
    DateTimeField.register_lookup(Date, 'date')
    CallRecord.objects.filter(
        start_time__date=some_date)

    CallRecord.objects.filter(
        GreaterThan('talk_time', 30)
        )

    CallRecord.objects.values(
        agent_name=F('agent__name'))

    CallRecord.objects.annotate(
        team=F('agent__name').concat(' AGENT').translate('de')
    )

    CallRecord.objects.filter(
        F.start_time.date.gte(some_date)
    )
