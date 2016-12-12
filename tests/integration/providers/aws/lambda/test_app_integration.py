from pytest import fixture
from tight.providers.aws.lambda_app import app
import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy
import importlib

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
    empty_controller =  importlib.import_module('fixtures.lambda_app.functions.empty_controller.handler')
    setattr(empty_controller, 'mock_get_handler', mock_function)
    empty_controller.mock_get_handler.func_globals['__package__'] = 'functions.empty_controller'
    empty_controller.mock_get_handler.func_globals['__name__'] = 'fixtures.lambda_app.functions.empty_controller.handler'
    lambda_proxy.get(empty_controller.mock_get_handler)
    result = empty_module.empty_controller({'body': None, 'httpMethod': 'GET'}, {})
    assert result['body'] == 'GOOD TO GO'