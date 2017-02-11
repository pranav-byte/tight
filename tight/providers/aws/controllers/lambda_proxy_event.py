# Copyright (c) 2017 lululemon athletica Canada inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import importlib
import json
import traceback
from functools import partial
from tight.core.logger import info

methods = [
    'get', 'post', 'patch', 'put', 'delete', 'options'
]


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class LambdaProxyController():
    HEADERS = {
        'Access-Control-Allow-Origin': '*'
    }

    def __init__(self):
        self.methods = {}
        for method in methods:
            def function(method, func, *args, **kwargs):
                self = kwargs.pop('self')
                self.attach_handler(func)
                controller_name = func.func_globals['__package__'].split('.')[-1]
                self.methods['{}:{}'.format(controller_name, method.upper())] = func
            setattr(self, method, partial(function, method, self=self))

    def attach_handler(self, func):
        function_package = func.func_globals['__name__']
        function_module = importlib.import_module(function_package)
        try:
            getattr(function_module, 'handler')
        except Exception as e:
            setattr(function_module, 'handler', self.run)

    def prepare_args(self, *args, **kwargs):
        event = args[1]
        context = args[2]
        if ('body' in event and event['body'] != None):
            try:
                event['body'] = json.loads(event['body'])
            except Exception as e:
                info(message='Could not json.loads ' + str(event['body']))
                event['body'] = {}
        try:
            principal_id = event['requestContext']['authorizer']['claims']['sub']
        except Exception as e:
            principal_id = None

        return {
            'event': event,
            'context': context,
            'principal_id': principal_id
        }

    def prepare_response(self, *args, **kwargs):
        if ('passthrough' in kwargs):
            return kwargs['passthrough']
        # Map return properties to the response.
        if ('body' not in kwargs):
            kwargs['body'] = {}
        elif (not isinstance(kwargs['body'], str)):
            kwargs['body'] = json.dumps(kwargs['body'])
        # Default response code is 200
        if ('statusCode' not in kwargs):
            kwargs['statusCode'] = 200
        # Response header needs to specify `Access-Control-Allow-Origin` in order
        # for CORS to function properly.
        if ('headers' not in kwargs):
            kwargs['headers'] = {}

        headers = merge_dicts(kwargs['headers'], self.HEADERS)
        kwargs['headers'] = headers
        # Ship it!
        return kwargs

    def run(self, *args, **kwargs):
        controller_name = args[0]
        event = args[1]
        context = args[2]
        method = event['httpMethod']
        method_handler = self.methods[':'.join([controller_name, method])]
        method_handler_args = self.prepare_args(*args, **kwargs)
        try:
            method_response = method_handler(*args, **method_handler_args)
        except Exception as e:
            # Really should check error type
            method_response = e.message
        if type(method_response) is dict:
            prepared_response = self.prepare_response(**method_response)
        else:
            raise Exception(method_response)
        return prepared_response

LambdaProxySingleton = LambdaProxyController()

current_module = sys.modules[__name__]


def expose():
    for method in methods:
        handler = getattr(LambdaProxySingleton, method)
        setattr(current_module, method, handler)
expose()


def set_default_headers(headers):
    LambdaProxySingleton.HEADERS = headers


def handler(*args, **kwargs):
    """ Proxy to LambdaProxySingleton::run

    :param args:
    :param kwargs:
    :return: LambdaProxyController
    """
    return LambdaProxySingleton.run(*args, **kwargs)
