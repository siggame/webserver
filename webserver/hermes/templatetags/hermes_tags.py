from django import template
from django.template.defaultfilters import stringfilter

from competition.models.game_model import Game

import slumber
import datetime
import logging
import requests

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
@stringfilter
def iso_to_datetime(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return ""


class CheckEmbargoedNode(template.Node):
    def __init__(self, team, variable_name):
        self.team = team
        self.variable_name = variable_name

    def render(self, context):
        team = context[self.team]
        try:
            # Get the last game played
            last_game = team.game_set.latest()

            # Grab the API url from the last Game that was played
            url = last_game.data['api_url']

            # Query API
            response = slumber.API(url).client.get(name=team.slug)

            # Make sure that we only get one client item back.
            assert response['meta']['total_count'] == 1

            # Get "embargoed" from returned client
            if response['objects'][0]['embargoed']:
                result = "embargoed"
            else:
                result = "unembargoed"
        except Game.DoesNotExist:
            result = "not ready"
        except slumber.exceptions.ImproperlyConfigured:
            result = "error"
            logger.error("Bad arena URL: {}".format(url))
        except (TypeError, KeyError), e:
            result = "error"
            logger.error("Error grabbing game data: {}".format(str(e)))
        except slumber.exceptions.HttpClientError:
            result = "error"
            logger.error("Couldn't connect to arena api ({})".format(url))
        except requests.exceptions.ConnectionError:
            result = "error"
            logger.error("Connection to arena api timed out ({})".format(url))
        except AssertionError:
            result = "error"
            if response['meta']['total_count'] > 1:
                msg = 'Found more than one team with slug "{}" in arena'
            else:
                msg = 'Found zero teams with slug "{}" in arena'
            logger.error(msg.format(team.slug))

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
