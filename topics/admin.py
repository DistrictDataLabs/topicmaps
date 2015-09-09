# topics.admin
# Admin site registration of models for editing.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Sep 08 20:59:50 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin site registration of models for editing.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from topics.models import Topic

##########################################################################
## Model Registration
##########################################################################

admin.site.register(Topic)
