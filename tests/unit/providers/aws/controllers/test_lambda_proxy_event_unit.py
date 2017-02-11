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

from tight.providers.aws.controllers.lambda_proxy_event import LambdaProxyController
from tight.providers.aws.controllers.lambda_proxy_event import LambdaProxySingleton
from tight.providers.aws.controllers.lambda_proxy_event import set_default_headers


def test_prepare_args_no_boom():
    instance = LambdaProxyController()
    prepared_args = instance.prepare_args('', {}, {})
    assert prepared_args == {'event': {}, 'context': {}, 'principal_id': None}


def test_prepare_args_json_loads_body():
    instance = LambdaProxyController()
    prepared_args = instance.prepare_args('', {'body': '{"name":"banana"}'}, {})
    assert prepared_args == {'event': {'body': {'name': 'banana'}}, 'context': {}, 'principal_id': None}


def test_prepare_args_json_loads_body_unparsable():
    instance = LambdaProxyController()
    prepared_args = instance.prepare_args('', {'body': 'I am just a string'}, {})
    assert prepared_args == {'event': {'body': {}}, 'context': {}, 'principal_id': None}


def test_prepare_response_passthrough():
    instance = LambdaProxyController()
    prepared_response = instance.prepare_response(passthrough='Banana')
    assert prepared_response == 'Banana'


def test_prepare_response_default():
    instance = LambdaProxyController()
    prepared_response = instance.prepare_response()
    assert prepared_response == {'body': {}, 'headers': {'Access-Control-Allow-Origin': '*'}, 'statusCode': 200}


def test_set_headers():
    set_default_headers({})
    prepared_response = LambdaProxySingleton.prepare_response()
    assert prepared_response == {'body': {}, 'headers': {}, 'statusCode': 200}
    set_default_headers({'Content-Type': 'text/html'})
    prepared_response = LambdaProxySingleton.prepare_response()
    assert prepared_response == {'body': {}, 'headers': {'Content-Type': 'text/html'}, 'statusCode': 200}
