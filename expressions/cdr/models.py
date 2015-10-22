from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Agent(models.Model):
    """
    An agent is an employee that takes calls.
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team)

    def __str__(self):
        return self.name


class CallRecord(models.Model):
    agent = models.ForeignKey(Agent)
    talk_time = models.PositiveIntegerField(
        help_text='Number of seconds the agent was talking to the customer'
    )
    hold_time = models.PositiveIntegerField(
        help_text='Number of seconds the agent had the customer on hold'
    )
    wrap_time = models.PositiveIntegerField(
        help_text='Number of seconds the agent spent in after call work'
    )
    start_time = models.DateTimeField(
        help_text='The date and time that the call began'
    )

    @property
    def handle_time(self):
        return self.talk_time + self.hold_time + self.wrap_time

    def __str__(self):
        return "CallRecord(agent={}, date={}, handle_time={})".format(
            self.agent, self.start_time, self.handle_time
        )
