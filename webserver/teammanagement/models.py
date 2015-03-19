from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from competition.models import (Team,
                                Registration,
                                RegistrationQuestion)

import logging

logger = logging.getLogger(__name__)


def check_student_status(team, registrations):
    """Checks a team's members and sets the team's eligible_to_win field
    according to their registrations

    Teams who have at least one non-student member are not eligible to
    win prizes

    """
    try:
        # Our fixture `fixtures/initial_data.yaml` creates this
        # question with the same choices and PK every time.
        q = RegistrationQuestion.objects.get(pk=4)
        no = q.question_choice_set.get(pk=12)

        # Just in case, though...
        assert "educational institution" in q.question
        assert no.choice == "No"
    except AssertionError:
        msg = 'Registration question/choice "{}"/"{}" does not match expected form'
        logger.error(msg.format(q.question, no.choice))
        return
    except RegistrationQuestion.DoesNotExist:
        logger.error("Could not find student question in database")
        return

    non_student_registrations = registrations.filter(
        response_set__question=q,
        response_set__choices=no
    )

    print non_student_registrations

    # If they're marked as eligible to win and they have non-students,
    # mark them as ineligible.
    if team.eligible_to_win and non_student_registrations.exists():
        team.eligible_to_win = False
        team.save()
        logger.info('Marked {} as ineligible to win'.format(team.name))

    if not team.eligible_to_win and not non_student_registrations.exists():
        team.eligible_to_win = True
        team.save()
        logger.info('Marked {} as eligible to win'.format(team.name))



@receiver(m2m_changed, sender=Team.members.through)
def check_eligibility(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Verify that teams are eligible to win prizes"""

    # Get all active registrations for this team
    team_registrations = Registration.objects.filter(
        active=True,
        user__team=instance,
        competition=instance.competition
    )

    # Mark eligibility according to student status
    check_student_status(instance, team_registrations)
