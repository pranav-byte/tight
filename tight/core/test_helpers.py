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
import os
import sys
import importlib
import yaml
import json
import shutil
from botocore import session as boto_session
from tight.providers.aws.clients import boto3_client
from tight.providers.aws.clients import dynamo_db
import placebo


@pytest.fixture
def app():
    return importlib.import_module('app_index')


@pytest.fixture
def event():
    with open('tests/fixtures/lambda_proxy_event.yml') as data_file:
        event = yaml.load(data_file)
    return event


def placebos_path(file, namespace, mode='playback'):
    test_path = '/'.join(file.split('/')[0:-1])
    placebo_path = '/'.join([test_path, 'placebos'])
    namespaced_path = '{}/{}'.format(placebo_path, namespace)
    if mode == 'record':
        if os.path.exists(namespaced_path):
            shutil.rmtree(namespaced_path)
            os.mkdir(namespaced_path)
        else:
            os.mkdir(namespaced_path)
    return namespaced_path


def spy_on_session(file, session, placebo_path):
    pill = placebo.attach(session, data_path=placebo_path)
    return pill


def prepare_pills(mode, placebo_path, dynamo_db_session):
    this = sys.modules[__name__]
    if not hasattr(this, 'pill') or not hasattr(this, 'boto3_pill'):
        boto3_session = boto3_client.session()
        boto3_pill = spy_on_session(file, boto3_session, placebo_path)
        boto3_pill_method = getattr(boto3_pill, mode)
        boto3_pill_method()
        pill = spy_on_session(file, dynamo_db_session, placebo_path)
        pill_method = getattr(pill, mode)
        pill_method()
        setattr(this, 'pill', pill)
        setattr(this, 'boto3_pill', boto3_pill)
    else:
        pill = getattr(this, 'pill')
        pill._data_path = placebo_path
        boto3_pill = getattr(this, 'boto3_pill')
        boto3_pill._data_path = placebo_path
        pill_method = getattr(pill, mode)
        pill_method()
        boto3_pill_method = getattr(boto3_pill, mode)
        boto3_pill_method()


def tape_deck(mode, file, dynamo_db_session, namespace):
    placebo_path = placebos_path(file, namespace, mode=mode)
    os.environ[mode.upper()] = 'True'
    prepare_pills(mode, placebo_path, dynamo_db_session)


def record(file, dynamo_db_session, namespace):
    tape_deck('record', file, dynamo_db_session, namespace)


def playback(file, dynamo_db_session, namespace):
    tape_deck('playback', file, dynamo_db_session, namespace)


def expected_response_body(dir, expectation_file, actual_response):
    file_path = '/'.join([dir, expectation_file])
    if 'PLAYBACK' in os.environ and os.environ['PLAYBACK'] == 'True':
        return json.loads(yaml.load(open(file_path))['body'])
    if 'RECORD' in os.environ and os.environ['RECORD'] == 'True':
        stream = file(file_path, 'w')
        yaml.safe_dump(actual_response, stream)
        return json.loads(actual_response['body'])


@pytest.fixture
def dynamo_db_session():
    session = getattr(dynamo_db, 'session') or None
    if session:
        return session
    else:
        session = boto_session.get_session()
        session.events = session.get_component('event_emitter')
        dynamo_db.session = session
        return session
