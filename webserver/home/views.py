from django.views.generic import TemplateView

from competition.models import Competition


class HomePageView(TemplateView):
    template_name = "home/home.html"
    
    def get_context_data(self, **kwargs):
      context = super(HomePageView, self).get_context_data(**kwargs)
      context["registered_competitions"] = Competition.objects.exclude(is_running=False, is_open=False)
      context["closed_competitions"] = Competition.objects.filter(is_running=False, is_open=False)
      return context

