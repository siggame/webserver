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
