from django.views.generic import TemplateView

from competition.models import Competition


class HomePageView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        context["open_competitions"] = Competition.objects.filter(is_open=True)
        context["running_competitions"] = Competition.objects.filter(is_running=True)
        context["next_competition"] = Competition.objects.first()

        if not self.request.user.is_anonymous():
            my_competitions = Competition.objects.user_registered(self.request.user)
            context["registered_competitions"] = my_competitions.exclude(is_running=False, is_open=False)
            context["closed_competitions"] = my_competitions.filter(is_running=False, is_open=False)
        return context

    def get_template_names(self):
        if self.request.user.is_anonymous():
            return ['home/unauthenticated.html']
        return ['home/authenticated.html']
