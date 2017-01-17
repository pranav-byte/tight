# Copyright (c) 2016 Michael Orion McManus
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
import pytest
from pytest import fixture
from tight.providers.aws.lambda_app import app

@fixture(autouse=True)
def set_region(monkeypatch):
    monkeypatch.setenv('TIGHT.APP_ROOT', 'fixtures/lambda_app')

def test_collect_controllers():
    controllers = app.collect_controllers()
    assert controllers == [{'empty_controller': 'fixtures.lambda_app.functions.empty_controller.handler'},{'fake_lambda_proxy_controller': 'fixtures.lambda_app.functions.fake_lambda_proxy_controller.handler'}]

def test_app_run_success():
    def successful_create(module):
        assert True, 'App is created'
    app.create = successful_create
    sys.modules.setdefault('app_index', True)
    app.run()

def test_app_run_failure():
    with pytest.raises(Exception):
        sys.modules.setdefault('app_index', True)
        def create_failure(module):
            raise Exception
        app.create = create_failure
        app.run()
