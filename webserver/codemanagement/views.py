from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from competition.views.mixins import RequireRunningMixin, CompetitionViewMixin

from .models import BaseClient, TeamClient
from .forms import TeamRepoForm


class CreateRepoView(CompetitionViewMixin,
                     RequireRunningMixin,
                     CreateView):
    model = TeamClient
    form_class = TeamRepoForm
    template_name = "codemanagement/create_team_repo.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateRepoView, self).dispatch(*args, **kwargs)

    def get_team(self):
        c = self.get_competition()
        queryset = self.request.user.team_set
        # If the team doesn't exist, throw a 404
        return get_object_or_404(queryset, competition=c)

    def get_base_choices(self):
        # Only let the user choose from BaseClients for this
        # competition.
        return self.get_competition().baseclient_set.all()

    def get_form_kwargs(self):
        kwargs = super(CreateRepoView, self).get_form_kwargs()
        kwargs['instance'] = TeamClient(team=self.get_team())
        kwargs['base_clients'] = self.get_base_choices()
        return kwargs
