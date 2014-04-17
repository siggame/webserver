from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from competition.models import Team
from greta.models import Repository

from .models import TeamClient, TeamSubmission
from .forms import AuthForm
from .serializers import TeamClientSerializer, RepoSerializer, TeamSerializer


class RepoAuth(APIView):
    """Checks a Team's repository password. Please provide 'teamid' and
    'password' as query parameters.

    Returns an **HTTP 200** if successful, with a JSON object full of
    information.

    Returns an **HTTP 400** if the form is bad or if the
    teamid/password was wrong.

    """

    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        form = AuthForm(request.GET)
        if not form.is_valid():
            return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(pk=form.cleaned_data['teamid'])
            if team.teamclient.git_password == form.cleaned_data['password']:
                t = TeamClientSerializer(team.teamclient)
                return Response(t.data)
            else:
                # Bad password
                return Response("Bad username/password",
                                status=status.HTTP_404_NOT_FOUND)

        except Team.DoesNotExist:
            return Response("Team doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)
        except TeamClient.DoesNotExist:
            return Response("Team doesn't have a client yet",
                            status=status.HTTP_404_NOT_FOUND)

        return Response("You shouldn't be able to get here.",
                        status=status.HTTP_400_BAD_REQUEST)


class RepoPath(APIView):
    """Fetches repository information for a given team's id.

    The path argument should be a single number: the ID number of the
    team.

    **Important**: If ``is_ready`` is false, the repository doesn't
    actually exist yet. Attempting to clone it will result in unhappy
    times.

    Returns a JSON object filled with goodies.

    """

    permission_classes = (IsAdminUser,)

    def get(self, request, team_id, format=None):
        try:
            team = Team.objects.get(pk=team_id)
            r = RepoSerializer(team.teamclient.repository)
            return Response(r.data)

        except Team.DoesNotExist:
            return Response("Team doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)
        except TeamClient.DoesNotExist:
            return Response("TeamClient doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)
        except Repository.DoesNotExist:
            return Response("Repository doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)

        return Response("You shouldn't be able to get here.",
                        status=status.HTTP_400_BAD_REQUEST)


class RepoTagList(APIView):
    """Returns a list of repository tags for a given competition.

    The single path argument should be the slug of the desired
    competition.

    **NOTE**: If a team has yet to create a client/repository, they
    will not show up in this list.

    If the team hasn't tagged anything, then ``tag`` will be null.

    """

    permission_classes = (IsAdminUser,)

    def get(self, request, competition_slug, format=None):
        try:
            clients = TeamClient.objects.filter(team__competition__slug=competition_slug)
            return Response([TeamClientSerializer(c).data for c in clients])

        except Team.DoesNotExist:
            return Response("Team doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)
        except TeamClient.DoesNotExist:
            return Response("TeamClient doesn't exist",
                            status=status.HTTP_404_NOT_FOUND)
        return Response("You shouldn't be able to get here.",
                        status=status.HTTP_400_BAD_REQUEST)
