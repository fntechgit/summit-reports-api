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


from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
import requests, logging, time
from django.core.cache import cache


class TokenValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # skip auth
        # return self.get_response(request)

        if not 'access_token' in request.GET :
            return HttpResponseForbidden()

        access_token = request.GET.get('access_token')

        if not access_token:
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        # try get access_token from DB and check if not expired
        cache_access_token = cache.get('token')

        if cache_access_token is not None :
            return self.get_response(request)


        # Token instrospection
        response = requests.post(
            settings.IDP_BASE_URL + '/oauth2/token/introspection',
            auth=(settings.RS_CLIENT_ID,settings.RS_CLIENT_SECRET),
            params={'token' : access_token}
        )

        if response.status_code == requests.codes.ok :
            token_info = response.json()
            # print(token_info)
            cache.set("token", token_info, timeout=token_info['expires_in'])
        else :
            logging.getLogger('django').error('INVALID TOKEN')
            return HttpResponseForbidden()


        return self.get_response(request)



