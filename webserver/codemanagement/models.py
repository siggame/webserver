from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from competition.models import Competition, Team
from greta.models import Repository


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


class TeamClient(models.Model):
    """Represents a team's repository"""
    team = models.OneToOneField(Team)
    base = models.ForeignKey(BaseClient)
    repository = models.OneToOneField(Repository)


@receiver(pre_save, sender=BaseClient)
def create_base_repo(sender, instance, raw, **kwargs):
    """Creates a new, blank shell repo on disk"""
    instance.language_slug = slugify(instance.language)

    # If the BaseClient is brand new, pk will be none.
    if instance.pk is None and not raw:
        name = "{0}/{1}.git".format(instance.competition.slug,
                                    instance.language_slug)
        description = "{0} client for {1}".format(instance.competition.name,
                                                  instance.language)
        repo = Repository.objects.create(name=name, description=description,
                                         owner=instance)
        instance.repository = repo


@receiver(pre_save, sender=TeamClient)
def create_repo(sender, instance, raw, **kwargs):
    """Forks a BaseClient repository and saves it on disk"""
    # If the TeamClient is brand new, pk will be none.
    if instance.pk is None and not raw:
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


@receiver(post_delete, sender=BaseClient)
def delete_base_repo(sender, instance, **kwargs):
    """Deletes a base repo when the BaseClient is deleted"""
    # When a BaseClient gets deleted, delete its corresponding
    # repository, too.
    instance.repository.delete()


@receiver(post_delete, sender=TeamClient)
def delete_team_repo(sender, instance, **kwargs):
    """Deletes a base repo when the TeamClient is deleted"""
    # When a TeamClient gets deleted, delete its corresponding
    # repository, too.
    instance.repository.delete()
