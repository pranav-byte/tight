# Copyright (c) 2017 lululemon athleticaanada inc.
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
import importlib
from functools import wraps

from pytest import fixture
from tight.providers.aws.lambda_app import app
import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy


@fixture(autouse=True)
def set_region(monkeypatch):
    monkeypatch.setenv('TIGHT.APP_ROOT', 'fixtures/lambda_app')


def test_app_create(empty_module):
    def mock_function(*args, **kwargs):
        return {
            'statusCode': 200,
            'body': 'GOOD TO GO'
        }
    setattr(empty_module, 'mock_function', mock_function)
    app.create(empty_module)
    assert hasattr(empty_module, 'empty_controller'), 'The empty module has controller attributes.'
    empty_controller = importlib.import_module('fixtures.lambda_app.functions.empty_controller.handler')
    setattr(empty_controller, 'mock_get_handler', mock_function)
    setattr(empty_controller.mock_get_handler, '__module__', 'fixtures.lambda_app.functions.empty_controller.handler')
    lambda_proxy.get(empty_controller.mock_get_handler)
    result = empty_module.empty_controller({'body': None, 'httpMethod': 'GET'}, {})
    assert result['body'] == 'GOOD TO GO'


def test_app_404(empty_module):
    """
    Test the scenario where your handler is wrapped by another function, such as an access or capability checker.

    E.g.

    @lambda_proxy.get
    @check_access
    def get_handler(*args, **kwargs):
        pass

    We want the wrapper to be able to return a response.

    :param empty_module:
    :return:
    """
    def test_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            lambda_proxy.exit_with_response(404, {'body': 'Not found.', 'headers': {'Content-Type': 'text/html'}})
            return f(*args, **kwargs)
        return wrapper

    @test_wrapper
    def mock_function(*args, **kwargs):
        return {
            'statusCode': 200,
            'body': 'GOOD TO GO'
        }

    setattr(empty_module, 'mock_function', mock_function)
    app.create(empty_module)
    assert hasattr(empty_module, 'empty_controller'), 'The empty module has controller attributes.'
    empty_controller = importlib.import_module('fixtures.lambda_app.functions.empty_controller.handler')
    setattr(empty_controller, 'mock_get_handler', mock_function)
    setattr(empty_controller.mock_get_handler, '__module__', 'fixtures.lambda_app.functions.empty_controller.handler')
    lambda_proxy.get(empty_controller.mock_get_handler)
    result = empty_module.empty_controller({'body': None, 'httpMethod': 'GET'}, {})
    assert result == {'body': 'Not found.', 'statusCode': 404, 'headers': {'Content-Type': 'text/html', 'Access-Control-Allow-Origin': '*'}}
