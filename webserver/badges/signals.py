from brabeion import badges
from django.db.models.signals import post_save
from django.dispatch import receiver
from competition.models import Competition

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Competition)
def check_competition_badges(sender, instance, created, raw, **kwargs):
    logger.debug("Competition saved")
    if not created and not instance.is_running and not instance.is_open:
        for team in instance.team_set.all():
            for user in team.members.all():
                badges.possibly_award_badge("competition_finished", user=user)
    
