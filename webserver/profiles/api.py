from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        return obj.get_absolute_url()


class ProfileListAPIView(generics.ListAPIView):
    """Lists Profiles on the site

    Returns an **HTTP 200** if successful, with a JSON object full of
    information.

    """
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserProfile.objects.exclude(user__pk=-1)
