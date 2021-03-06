# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone

from . import serializers
from . import permissions
from . import models
from .authentication import ExpiringTokenAuthentication
from .authentication import get_client

logger = logging.getLogger('django')

class ObtainExpiringAuthToken(ObtainAuthToken):
    """Returns a ScrumScrumUserToken.

    Depending on the type of client specified in the HTTP_CLIENT header,
    this will either return a token with an expiration or one without.
    Mobile-applications will get a lifetime token, while web-based clients
    will get a token that will eventually expire. Change TOKEN_EXPIRATION_DAYS
    in django.conf.settings to modify the number of days a web-client token
    will be valid.
    """

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            try:
                #   Try to get the client type ('web' or 'mobile')
                client = get_client(request)
            except ValueError as e:
                #   There was a problem with the client format in the
                #   HTTP header
                return Response({
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            token, created = \
                models.ScrumScrumUserToken.objects.get_or_create(user=user,
                                                                 client=client)

            if not created:
                #   We've created a new token, set the `created_on` field
                #   to the current UTC time
                token.created_on = timezone.now()
                token.save()

            #   Give the token to the client
            return Response({"token": token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """Verifies user credentials and returns an authentication token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainExpiringAuthToken().post(request)

class ScrumScrumUserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, and updating scrum scrum users."""

    serializer_class = serializers.ScrumScrumNewUserSerializer
    queryset = models.ScrumScrumUser.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.UpdateOwnUser,)

    def get_serializer_class(self):
        """Configure the right serializer depending on URL request method.

        We want to make sure that all ScrumScrumUser fields are exposed on the
        POST method (creating new users), but we don't want current users to
        update certain information such as their username (PUT/PATCH methods).
        """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = serializers.ScrumScrumUpdateUserSerializer

        return serializer_class
