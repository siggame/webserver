"""Settings file for project deployment

"""
from webserver.settings.defaults import *

# Choose which site we're using. initial_data.yaml installs some
# fixture data so that localhost:8000 has SIDE_ID == 1, and
# megaminerai.com has SITE_ID == 2
#
# Since we're deploying on megaminerai.com, SITE_ID should be 2.
SITE_ID = 2
