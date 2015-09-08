# topicmaps.settings.development
# The Django settings for TopicMaps in development
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:19:25 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: development.py [] bbengfort@districtdatalabs.com $

"""
The Django settings for TopicMaps in development
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Secret Key doesn't matter in Dev
SECRET_KEY       = 'cyt*c1@%sg6j@g6y9fdrd@iakg7)ek!dqb@7grl(c-nkm%2596'

## Content
MEDIA_ROOT       = os.path.join(PROJECT, 'media')
STATIC_ROOT      = 'staticfiles'
