from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from models import UserProfile
from forms import UserProfileForm


class ProfileListView(ListView):
    """ A view that displays a user's profile.
    """
    template_name = "accounts/list_profile.html"
    model = UserProfile
    context_object_name = "userprofiles"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        return super(ProfileListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return UserProfile.objects.order_by('user__username')


class ProfileView(DetailView):
    """ A view that displays a user's profile.
    """
    template_name = "accounts/view_profile.html"
    context_object_name = "userprofile"
    model = UserProfile

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(user__username=self.kwargs['username'])


class MyProfileView(ProfileView):
    """ A view that displays a user's own profile.
    """
    def get_object(self, queryset=None):
        return self.request.user.get_profile()


class ProfileUpdateView(UpdateView):
    """ A view that displays a form for editing a user's profile.
    """
    template_name = "accounts/update_profile.html"
    form_class = UserProfileForm
    context_object_name = "userprofile"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.get_profile()

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Profile updated")
        return super(ProfileUpdateView, self).form_valid(form)
