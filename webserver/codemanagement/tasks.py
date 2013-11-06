from celery import task
from celery.result import AsyncResult

from competition.models import (Team, RegistrationQuestion,
                                RegistrationQuestionResponse)

from .models import TeamSubmission

import logging

logger = logging.getLogger(__name__)


@task()
def create_shellai_tag(instance):
    """Tags the repo's HEAD as "ShellAI" to provide a default tag for
    the arena to use"""
    team_name = instance.team.name

    if instance.repository.task_id is not None:
        # Wait for the repo to be created
        msg = "Waiting for {}'s repository to be created..."
        logger.info(msg.format(team_name))
        AsyncResult(instance.repository.task_id).wait()

    logger.info("{}'s repository is ready".format(team_name))

    try:
        commit = instance.repository.repo['HEAD']
    except KeyError:
        # Log an error if we can't get a commit
        msg = "Unable to tag {}'s repo. Bad ref 'HEAD'. Is the repo empty?"
        logger.error(msg.format(team_name))
    else:
        # Create a submission for the HEAD commit
        TeamSubmission.objects.create(teamclient=instance,
                                      commit=commit.id,
                                      name="ShellAI",
                                      submitter=None)
        logger.info("Tagged {}'s repo".format(team_name))

@task()
def mark_all_ineligible():
    """Marks teams with non-student members as ineligible"""

    question = "Are you currently a full time student?"
    try:
        q = RegistrationQuestion.objects.get(question=question)
        no = q.question_choice_set.get(choice="No")
        responses = RegistrationQuestionResponse.objects.filter(question=q,
                                                                choices=no)
    except RegistrationQuestion.DoesNotExist:
        logger.error('No such question "{}"'.format(question))

    if not responses.exists():
        logger.info("No nonstudents found")
        return

    count = 0
    for response in responses:
        try:
            reg = response.registration
            team = Team.objects.get(competition=reg.competition,
                                    members=reg.user)
            team.eligible_to_win = False
            team.save()
            count += 1
        except Team.DoesNotExist:
            continue

    logger.info('Marked {} teams ineligible to win'.format(count))
