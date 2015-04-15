from rest_framework import serializers
from greta.models import Repository
from competition.models import Team

from .models import TeamClient, TeamSubmission


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'slug', 'eligible_to_win')


class RepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ('name', 'description', 'forked_from',
                  'path', 'is_ready')

    forked_from = serializers.RelatedField(read_only=True)
    path = serializers.SerializerMethodField(read_only=True)
    is_ready = serializers.SerializerMethodField(read_only=True)

    def get_path(self, repo):
        return repo.path

    def get_is_ready(self, repo):
        return repo.is_ready()


class TeamSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamSubmission
        fields = ('name', 'commit')


class TeamClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamClient
        fields = ('team', 'repository', 'tag', 'language')

    team = TeamSerializer()
    repository = RepoSerializer()
    tag = serializers.SerializerMethodField(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)

    def get_tag(self, teamclient):
        try:
            latest_sub= teamclient.submissions.latest()
            return TeamSubmissionSerializer(latest_sub).data
        except TeamSubmission.DoesNotExist:
            return None

    def get_language(self, teamclient):
        return teamclient.base.language
