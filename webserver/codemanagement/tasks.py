from celery import task
from celery.result import AsyncResult

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
        AsyncResult(instance.repository.task_id).wait()
        msg = "Waiting for {}'s repository to be created..."
        logger.info(msg.format(team_name))

    logger.info("{}'s repository is ready".format(team_name))

    # Create a submission for the HEAD commit
    TeamSubmission.objects.create(team=instance.team,
                                  commit=instance.repository.repo['HEAD'].id,
                                  name="ShellAI",
                                  submitter=None)
    logger.info("Tagged {}'s repo".format(team_name))
