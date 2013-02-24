from django.views.generic.edit import CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404

from competition.views.mixins import RequireRunningMixin, CompetitionViewMixin
from competition.models import Team

from .models import BaseClient, TeamClient
from .forms import TeamRepoForm


class CreateRepoView(CompetitionViewMixin,
                     RequireRunningMixin,
                     CreateView):
    model = TeamClient
    form_class = TeamRepoForm
    template_name = "codemanagement/create_team_repo.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs    # Needed by get_competition()

        try:
            competition = self.get_competition()
            self.request.user.team_set.get(competition=competition)
        except Team.DoesNotExist:
            msg = "Please join a team before creating a repository"
            messages.info(request, msg)
            return redirect('team_create', comp_slug=competition.slug)

        return super(CreateRepoView, self).dispatch(request, *args, **kwargs)

    def get_team(self):
        c = self.get_competition()
        # If the team doesn't exist, throw a 404
        team = get_object_or_404(self.request.user.team_set,
                                 competition=c)
        try:
            team.teamclient     # This should raise an exception
        except TeamClient.DoesNotExist:
            return team

        # If an exception wasn't raised, it means that the user
        # already has a TeamClient and repository
        raise Http404("User's team already has a repository")

    def get_base_choices(self):
        # Only let the user choose from BaseClients for this
        # competition.
        return self.get_competition().baseclient_set.all()

    def get_form_kwargs(self):
        kwargs = super(CreateRepoView, self).get_form_kwargs()
        kwargs['instance'] = TeamClient(team=self.get_team())
        kwargs['base_clients'] = self.get_base_choices()
        return kwargs
