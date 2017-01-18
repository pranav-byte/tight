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
