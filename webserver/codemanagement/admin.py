from django.contrib import admin

from competition.models import Competition, Team
from competition.admin import CompetitionAdmin, TeamAdmin

from .models import BaseClient, TeamClient, TeamSubmission


class TeamClientInlineAdmin(admin.TabularInline):
    model = TeamClient


class TeamSubmissionInlineAdmin(admin.TabularInline):
    model = TeamSubmission


class BaseClientInlineAdmin(admin.TabularInline):
    model = BaseClient
    fields = ('language', 'language_slug', 'repository')
    readonly_fields = ('repository',)
    prepopulated_fields = {"language_slug": ("language",)}


#######################################################################
# Override the Competition and Team admins to show repository
# information as well
#######################################################################

class ProgrammingCompetitionAdmin(CompetitionAdmin):
    inlines = CompetitionAdmin.inlines + (BaseClientInlineAdmin,)


class ProgrammingTeamAdmin(TeamAdmin):
    inlines = TeamAdmin.inlines + [TeamClientInlineAdmin,
                                   TeamSubmissionInlineAdmin]


admin.site.unregister(Team)
admin.site.unregister(Competition)

admin.site.register(Team, ProgrammingTeamAdmin)
admin.site.register(Competition, ProgrammingCompetitionAdmin)
