from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

from competition.models import Team

import json


class TeamStats(models.Model):
    team = models.OneToOneField(Team)
    data_field = models.TextField(null=True, default="null")


    @property
    def data(self):
        return json.loads(self.data_field)

    @data.setter
    def data(self, value):
        self.data_field = json.dumps(value)
