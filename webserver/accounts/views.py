from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from models import UserProfile
from forms import UserProfileForm


class ProfileListView(ListView):
    """ A view that displays a user's profile.
    """
    template_name = "accounts/list_profile.html"
    model = UserProfile
    context_object_name = "userprofiles"


class ProfileMixin(SingleObjectMixin):
    """Provides views with the current user's profile
    """
    model = UserProfile
    context_object_name = "userprofile"

    def get_object(self):
        return self.request.user.get_profile()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        return super(ProfileMixin, self).dispatch(request, *args, **kwargs)


class ProfileView(ProfileMixin, DetailView):
    """ A view that displays a user's profile.
    """
    template_name = "accounts/view_profile.html"


class ProfileUpdateView(ProfileMixin, UpdateView):
    """ A view that displays a form for editing a user's profile.
    """
    template_name = "accounts/update_profile.html"
    form_class = UserProfileForm

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

