from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User

from guardian.shortcuts import assign_perm, remove_perm, get_groups_with_perms

from competition.models import Competition, Team
from greta.models import Repository

from dulwich.objects import Tag, parse_timezone

from .exceptions import CodeManagementException
from .validators import sha1_validator, tag_validator

from hashlib import sha1
from os import urandom

import re
import time
import logging
import datetime

logger = logging.getLogger(__name__)


def generate_unusable_password():
    return sha1(urandom(100)).hexdigest()[:15]


class BaseClient(models.Model):
    """Represents a shell repository, which the SIG-Game devs will set
    up. These repos get forked to create competitor repositories
    (TeamClients)"""
    competition = models.ForeignKey(Competition)
    language = models.CharField(max_length=20,
                                verbose_name="Programming Language")
    language_slug = models.SlugField(blank=True)
    repository = models.OneToOneField(Repository)

    def __unicode__(self):
        return "{0} client".format(self.language)

    @models.permalink
    def get_absolute_url(self):
        return ('repo_detail', (), {'pk': self.repository.pk})


class TeamClient(models.Model):
    """Represents a team's repository"""
    team = models.OneToOneField(Team)
    base = models.ForeignKey(BaseClient)
    repository = models.OneToOneField(Repository)
    git_password = models.CharField(max_length=100,
                                    default=generate_unusable_password)

    @models.permalink
    def get_absolute_url(self):
        return ('repo_detail', (), {'pk': self.repository.pk})

    def git_clone_command(self):
        data = {
            'protocol': settings.GIT_PROTOCOL,
            'host': settings.GIT_HOST,
            'port': settings.GIT_PORT,
            'user': '{slug}-{id}'.format(slug=self.team.slug, id=self.team.pk),
            'repo_name': re.sub(r'__\d+\.git$', '.git', self.repository.name)
        }
        cmd = "git clone {protocol}://{user}@{host}:{port}/{repo_name}"
        return cmd.format(**data)


class TeamSubmission(models.Model):
    class Meta:
        unique_together = (
            ('teamclient', 'name'),
        )
        ordering = ['-tag_time']
        get_latest_by = 'submission_time'

    teamclient = models.ForeignKey(TeamClient, related_name="submissions")
    commit = models.CharField(max_length=40,
                              validators=[sha1_validator])
    name = models.CharField(max_length=50,
                            validators=[tag_validator],
                            help_text="Choose a name for this submission")
    submitter = models.ForeignKey(User, null=True, blank=True)
    tag_time = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(auto_now_add=True)

    @property
    def bytestring_name(self):
        return self.name.encode('latin-1')

    @property
    def bytestring_commit(self):
        return self.commit.encode('latin-1')


@receiver(pre_save, sender=BaseClient)
def create_base_repo(sender, instance, raw, **kwargs):
    """Creates a new, blank shell repo on disk"""
    if instance.language_slug == "":
        instance.language_slug = slugify(instance.language)

    # If the BaseClient is brand new, pk will be none.
    if instance.pk is None and not raw:
        logger.info("Creating BaseClient repository")
        name = "{0}/{1}.git".format(instance.competition.slug,
                                    instance.language_slug)
        description = "{0} client for {1}".format(instance.competition.name,
                                                  instance.language)
        repo = Repository.objects.create(name=name, description=description,
                                         owner=instance)
        instance.repository = repo
        logger.info("Created BaseClient repository")


@receiver(pre_save, sender=TeamClient)
def create_team_repo(sender, instance, raw, **kwargs):
    """Forks a BaseClient repository and saves it on disk"""
    # If the TeamClient is brand new, pk will be none.
    if instance.pk is None and not raw:
        logger.info("Creating TeamClient repository")
        name = "{0}/{1}__{2}.git".format(instance.team.competition.slug,
                                         instance.team.slug,
                                         instance.team.pk)
        desc = "{0}'s {1} client for {2}".format(instance.team.name,
                                                 instance.base.language,
                                                 instance.team.competition.name)
        default_branch = instance.base.repository.default_branch
        repo = Repository.objects.create(name=name,
                                         description=desc,
                                         default_branch=default_branch,
                                         forked_from=instance.base.repository,
                                         owner=instance)
        instance.repository = repo
        logger.info("TeamClient repository created")

    # Give the team access to their repo
    assign_perm('can_view_repository', instance.team.get_group(),
           instance.repository)


@receiver(post_save, sender=BaseClient)
def set_base_repo_owner(sender, instance, created, raw, **kwargs):
    """Sets the BaseClient's repository owner to the BaseClient"""
    if instance.repository.owner is None:
        instance.repository.owner = instance
        instance.repository.save()


@receiver(post_save, sender=TeamClient)
def teamclient_post_save(sender, instance, created, raw, **kwargs):
    """Sets the TeamClient's repository owner to the TeamClient and
    creates a TeamSubmission for ShellAI"""
    if instance.repository.owner is None:
        instance.repository.owner = instance
        instance.repository.save()
    if created and not raw:
        from .tasks import create_shellai_tag
        create_shellai_tag.delay(instance)


@receiver(post_delete, sender=BaseClient)
def delete_base_repo(sender, instance, **kwargs):
    """Deletes a base repo when the BaseClient is deleted"""
    # When a BaseClient gets deleted, delete its corresponding
    # repository, too.
    try:
        logger.info("Deleting BaseClient repository")
        instance.repository.delete()
    except Repository.DoesNotExist:
        logger.info("Repository was already deleted")


@receiver(post_delete, sender=TeamClient)
def delete_team_repo(sender, instance, **kwargs):
    """Deletes a base repo when the TeamClient is deleted"""
    # When a TeamClient gets deleted, delete its corresponding
    # repository, too.
    try:
        logger.info("Deleting TeamClient repository")
        # For each group that has permissions to access this
        # repository, remove its permissons.
        for group in get_groups_with_perms(instance.repository):
            logger.info("Removing repo view permissions from %s" % group.name)
            remove_perm('can_view_repository', group, instance.repository)
        instance.repository.delete()
    except Repository.DoesNotExist:
        logger.info("Repository was already deleted")


@receiver(pre_save, sender=TeamSubmission)
def tag_commit(sender, instance, raw, **kwargs):
    """Adds a git tag to a repository"""
    team = instance.teamclient.team
    repository = instance.teamclient.repository
    repo = repository.repo

    try:
        commit = repo[instance.bytestring_commit]
    except KeyError:
        msg = "No such commit with sha {}".format(instance.bytestring_commit)
        raise CodeManagementException(msg)

    instance.tag_time = datetime.datetime.now()

    msg = "Tagged via the SIG-Game website"
    if instance.submitter:
        msg = "Tagged by {} via the SIG-Game website".format(instance.submitter)

    # Create an annotated tag
    tag = Tag()
    tag.tagger = "SIG-Game <siggame@mst.edu>"
    tag.message = msg
    tag.name = instance.bytestring_name
    tag.object = (commit, commit.id)
    tag.tag_time = int(time.mktime(instance.tag_time.timetuple()))
    tag.tag_timezone, _ = parse_timezone('-0600')

    # Save it in the repo
    repo.object_store.add_object(tag)
    repo['refs/tags/' + tag.name] = tag.id

    # Create a log message
    log_msg = 'Tag added to {}\'s repo ({}) on commit {} with message "{}"'
    logger.info(log_msg.format(team.name, repository.pk, commit.id, msg))
