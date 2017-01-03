import os
from tight.providers.aws.clients import dynamo_db

def test_no_boom():
    assert True, 'Client can be imported.'

def test_dynamo_db_connect_local():
    setattr(dynamo_db, 'engine', None)
    os.environ['AWS_REGION'] = 'us-west-99'
    os.environ['USE_LOCAL_DB'] = 'True'
    class EngineSpy(object):
        def connect(self, *args, **kwargs):
            assert kwargs.pop('host') == 'localhost', 'Connect to dynamo locally.'

        def connect_to_region(self, *args, **kwargs):
            raise Exception('Should not call this method.')

    setattr(dynamo_db, 'Engine', EngineSpy)
    dynamo_db.connect()

def test_dynamo_db_connect_ci():
    setattr(dynamo_db, 'engine', None)
    os.environ['AWS_REGION'] = 'us-west-99'
    os.environ['CI'] = 'True'
    os.environ.pop('USE_LOCAL_DB')
    class EngineSpy(object):
        def connect(self, *args, **kwargs):
            raise Exception('Should not call this method.')

        def connect_to_region(self, *args, **kwargs):
            assert 'session' in kwargs, 'Session is provided to engine.'

    setattr(dynamo_db, 'Engine', EngineSpy)
    dynamo_db.connect()

def test_dynamo_db_connect_prod():
    setattr(dynamo_db, 'engine', None)
    os.environ['AWS_REGION'] = 'us-west-99'
    os.environ.pop('CI')
    class EngineSpy(object):
        def connect(self, *args, **kwargs):
            raise Exception('Should not call this method.')

        def connect_to_region(self, *args, **kwargs):
            assert 'session' not in kwargs, 'Session is not provided to engine.'

    setattr(dynamo_db, 'Engine', EngineSpy)
    dynamo_db.connect()
