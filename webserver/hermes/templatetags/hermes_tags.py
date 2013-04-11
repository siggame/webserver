from django import template
from django.template.defaultfilters import stringfilter

import slumber

register = template.Library()


class CheckEmbargoedNode(template.Node):
    def __init__(self, team, variable_name):
        self.team = team
        self.variable_name = variable_name

    def render(self, context):
        team = context[self.team]
        last_game = team.game_set.latest()
        try:
            url = last_game.data['api_url']
            result = slumber.API(url).client.get(name=team.name)['embargoed']
        except KeyError:
            result = "error"

        context[self.variable_name] = result
        return ""


@register.tag
def check_embargoed(parser, token):
    try:
        tag_name, team, _as, variable = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        msg = '{0} should be "{0} <team> as <variable>"'
        raise template.TemplateSyntaxError(msg.format(tag_name))
    return CheckEmbargoedNode(team, variable)
