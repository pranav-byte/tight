from pytest import fixture
import importlib

@fixture
def empty_module():
    return importlib.import_module('fixtures.empty_module')