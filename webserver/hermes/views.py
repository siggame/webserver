from django.http import HttpResponse
import requests
import logging

logger = logging.getLogger(__name__)


def rating(request):
    url = "http://arena.megaminerai.com/mies/thunderdome/rate/"
    try:
        url = "/".join([url, request.GET['game_id'], request.GET['rating']])
        logger.info("Sending request to {}".format(url))
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Returned HTTP {}".format(response.status_code))
        return HttpResponse("Success")
    except KeyError:
        logger.warning("Cannot send request to arena. Missing query param.")
        return HttpResponse("Missing query params")
    except Exception, e:
        logger.warning("Miscellaneous error. {}".format(str(e)))
        return HttpResponse(str(e))
