# topicmaps.views
# Default application views for the system.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 13:20:11 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Default application views for the system.
"""

##########################################################################
## Imports
##########################################################################

import topicmaps

from datetime import datetime
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

##########################################################################
## Views
##########################################################################

class HomePageView(TemplateView):

    template_name = "site/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

##########################################################################
## API Views for this application
##########################################################################

class HeartbeatViewSet(viewsets.ViewSet):
    """
    Endpoint for heartbeat checking, including the status and version.
    """

    permission_classes = (AllowAny,)

    def list(self, request):
        return Response({
            "status": "ok",
            "version": topicmaps.get_version(),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })
