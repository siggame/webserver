from rest_framework import serializers
from greta.models import Repository
from competition.models import Team

from .models import TeamClient, TeamSubmission


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'slug')


class RepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ('name', 'description', 'forked_from',
                  'path', 'is_ready')

    forked_from = serializers.RelatedField()
    path = serializers.SerializerMethodField('get_path')
    is_ready = serializers.SerializerMethodField('get_is_ready')

    def get_path(self, repo):
        return repo.path

    def get_is_ready(self, repo):
        return repo.is_ready()


class TeamSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamSubmission


class TeamClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamClient
        fields = ('team', 'repository', 'tag')

    team = TeamSerializer()
    repository = RepoSerializer()
    tag = serializers.SerializerMethodField('get_tag')

    def get_tag(self, teamclient):
        try:
            tc = teamclient.submissions.latest().name
            return TeamSubmissionSerializer(tc)
        except TeamSubmission.DoesNotExist:
            return None
