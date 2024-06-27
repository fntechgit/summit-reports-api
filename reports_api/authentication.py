"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from django.http import HttpResponseForbidden
from django.conf import settings
import requests, logging, sys
from django.core.cache import cache


class TokenValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #return self.get_response(request)
        
        try:
            access_token = TokenValidationMiddleware.get_access_token(request)
            if access_token is None:
                logging.getLogger('django').warning('missing access token')
                return HttpResponseForbidden("Missing Access Token")
            # we got an access token on request

            token_info = TokenValidationMiddleware.get_token_info(access_token)
            # now check the scope
            if 'scope' in token_info:
                current_scope = token_info['scope']
                required_scope = settings.REQUIRED_SCOPES
                logging.getLogger('django').debug(
                    'current scope {current} required scope {required}'
                        .format(current=current_scope, required=required_scope)
                )

                # check scopes
                if len(set.intersection(set(required_scope.split()), set(current_scope.split()))):
                    return self.get_response(request)
                else:
                    return HttpResponseForbidden("Missing Scopes on Access Token")
        except:
            logging.getLogger('django').error(sys.exc_info())

        return HttpResponseForbidden()

    @staticmethod
    def get_access_token(request):
        auth = get_authorization_header(request).split()

        if len(auth) == 1:
            msg = 'Invalid bearer header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid bearer header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        if auth and auth[0].lower() == b'bearer':
            return auth[1]
        elif 'access_token' in request.POST:
            return request.POST['access_token']
        elif 'access_token' in request.GET:
            return request.GET['access_token']
        else:
            return None

    @staticmethod
    def get_token_info(access_token):
        """
        Authenticate the request, given the access token.
        """
        cached_token_info = None

        # try get access_token from DB and check if not expired
        cached_token_info = cache.get(access_token)

        if cached_token_info is None:
            try:
                response = requests.post(
                    '{base_url}/{endpoint}'.format(
                        base_url=settings.IDP_BASE_URL ,
                        endpoint=settings.IDP_INTROSPECTION_ENDPOINT
                    ),
                    auth=(settings.RS_CLIENT_ID, settings.RS_CLIENT_SECRET),
                    params={'token': access_token},
                    verify=settings.DEBUG
                )

                if response.status_code == requests.codes.ok:
                    cached_token_info = response.json()
                    cache.set(access_token, cached_token_info, timeout=cached_token_info['expires_in'])
                else:
                    logging.getLogger('django').warning(
                        'http code {code} http content {content}'.format(
                            code=response.status_code,
                            content=response.content
                        )
                    )
                    raise exceptions.AuthenticationFailed('invalid response')

            except requests.exceptions.RequestException as e:
                logging.getLogger('django').error(e)
                raise
            except:
                logging.getLogger('django').error(sys.exc_info())
                raise

        return cached_token_info


