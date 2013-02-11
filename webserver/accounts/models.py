from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

import markdown


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    about_me = models.TextField()
    rendered_about_me = models.TextField(editable=False,
                                         null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('view_profile', (), {'username': self.user.username})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=UserProfile)
def user_profile_pre_save(sender, instance, **kwargs):
    # Render the about_me field as HTML instead of markdown
    instance.rendered_about_me = markdown.markdown(instance.about_me)
