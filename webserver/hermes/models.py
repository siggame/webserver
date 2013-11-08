from django.db import models

from competition.models import Team

import json


class TeamStats(models.Model):
    team = models.OneToOneField(Team)
    updated = models.DateTimeField(auto_now=True)
    data_field = models.TextField(null=True, default="null")

    def __str__(self):
        return self.team.name

    @property
    def data(self):
        return json.loads(self.data_field)

    @data.setter
    def data(self, value):
        self.data_field = json.dumps(value)
