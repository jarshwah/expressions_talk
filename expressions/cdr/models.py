from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(
        Team, blank=True, null=True)

    def __str__(self):
        return self.name


class CallRecord(models.Model):
    agent = models.ForeignKey(Agent)
    talk_time = models.PositiveIntegerField()
    hold_time = models.PositiveIntegerField()
    wrap_time = models.PositiveIntegerField()
    start_time = models.DateTimeField()

    @property
    def handle_time(self):
        return (
            self.talk_time +
            self.hold_time +
            self.wrap_time
        )

    def __str__(self):
        return "date={}, handle_time={})".format(
            self.start_time,
            self.handle_time
        )
