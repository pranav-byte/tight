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

import pytest
import re
import tight
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


def test_proxy_controller_run_error_handling(monkeypatch):
    """ This looks like one big regex literal, however there are some control characters sprinkled in.
        Hopefully, this will be robust enough to not break frequently. However, if it does look for
        consider: Did the `lambda_proxy_event.py` module get moved? Did line numbers change enough that
        pattern to match them is no longer valid?
    """
    escaped_text = r"""\
\
Traceback\ \(most\ recent\ call\ last\)\:\
\_\_\ File\ \".*\/tight\/tight\/providers\/aws\/controllers\/lambda\_proxy\_event\.py\"\,\ line\ \d+,\ in\ run\
\_\_\_\_\ method\_response\ \=\ method\_handler\(\*args\,\ \*\*method\_handler\_args\)\
\_\_\ File\ \".*\/tight\/tests\/unit\/providers\/aws\/controllers\/test\_lambda\_proxy\_event\_unit\.py\"\,\ line\ \d+,\ in\ controller\_stub\
\_\_\_\_\ raise\ Exception\(\'I\ am\ an\ error\.\'\)\
Exception\:\ I\ am\ an\ error\."""

    traceback_assertion_pattern = re.compile(escaped_text)
    instance = LambdaProxyController()

    def controller_stub(*args, **kwargs):
        raise Exception('I am an error.')
    instance.methods['test_controller:GET'] = controller_stub

    def error_spy(*args, **kwargs):
        match = re.search(traceback_assertion_pattern, kwargs['message'])
        assert match is not None, 'Error is logged with formatted stacktrace.'
    monkeypatch.setattr(tight.providers.aws.controllers.lambda_proxy_event, 'error', error_spy)

    with pytest.raises(Exception) as ex:
        instance.run('test_controller', {'httpMethod': 'GET'}, {})

    assert str(ex.value) == 'There was an error.'
