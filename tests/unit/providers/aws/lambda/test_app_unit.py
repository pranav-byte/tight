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