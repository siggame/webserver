from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc

from competition.models import Team
from .models import TeamClient
from .forms import AuthForm


class RepoAuthHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        form = AuthForm(request.GET)
        if not form.is_valid():
            return rc.BAD_REQUEST

        try:
            team = Team.objects.get(pk=form.cleaned_data['teamid'])
            if team.teamclient.git_password == form.cleaned_data['password']:
                return {
                    'team': {
                        'id': team.id,
                        'name': team.name,
                        'slug': team.slug,
                    },
                    'repository': {
                        'name': team.teamclient.repository.name,
                        'path': team.teamclient.repository.path,
                        'description': team.teamclient.repository.description,
                        'base': team.teamclient.base.repository.name,
                    },
                }
            else:
                # Bad password
                return rc.FORBIDDEN

        except Team.DoesNotExist:
            return rc.NOT_FOUND
        except TeamClient.DoesNotExist:
            return rc.NOT_FOUND

        return rc.NOT_FOUND
