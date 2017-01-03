import os
import tight.core.test_helpers as test_helpers
from tight.providers.aws.clients import boto3_client

def test_no_boom():
    assert True, 'Module can be imported.'

def test_prepare_pills_record():
    test_helpers.prepare_pills('record', 'some/path', boto3_client.session())
    boto3_pill = getattr(test_helpers, 'boto3_pill')
    dynamo_pill = getattr(test_helpers, 'pill')
    # Do it again and make sure objects are the same
    test_helpers.prepare_pills('record', 'some/path', boto3_client.session())
    boto3_pill_cached = getattr(test_helpers, 'boto3_pill')
    dynamo_pill_cached = getattr(test_helpers, 'pill')
    assert boto3_pill == boto3_pill_cached, 'boto3 pill is cached'
    assert dynamo_pill == dynamo_pill_cached, 'dynamo pill is cached'

def test_prepare_pills_playback():
    test_helpers.prepare_pills('playback', 'some/path', boto3_client.session())
    boto3_pill = getattr(test_helpers, 'boto3_pill')
    dynamo_pill = getattr(test_helpers, 'pill')
    # Do it again and make sure objects are the same
    test_helpers.prepare_pills('playback', 'some/path', boto3_client.session())
    boto3_pill_cached = getattr(test_helpers, 'boto3_pill')
    dynamo_pill_cached = getattr(test_helpers, 'pill')
    assert boto3_pill == boto3_pill_cached, 'boto3 pill is cached'
    assert dynamo_pill == dynamo_pill_cached, 'dynamo pill is cached'

def test_placebos_path_playback():
    result = test_helpers.placebos_path('/some/absolute/path.py', 'my_namespace')
    assert result == '/some/absolute/placebos/my_namespace'

def test_placebos_path_record(tmpdir):
    test_file = '{}/some_test.py'.format(tmpdir)
    with file(test_file, 'w') as tmp_test_file:
        tmp_test_file.write('')

    tmpdir.mkdir('placebos')
    result = test_helpers.placebos_path(test_file, 'some_test', mode='record')

    assert result == '{}/placebos/some_test'.format(tmpdir)
    assert os.path.isdir(result), 'Namespaced placebos directory exists'

def test_placebos_path_record_placebos_exist(tmpdir):
    test_file = '{}/some_test.py'.format(tmpdir)
    with file(test_file, 'w') as tmp_test_file:
        tmp_test_file.write('')

    tmpdir.mkdir('placebos')
    result = test_helpers.placebos_path(test_file, 'some_test', mode='record')

    assert result == '{}/placebos/some_test'.format(tmpdir)
    assert os.path.isdir(result), 'Namespaced placebos directory exists'
    disappearing_file = '{}/i_should_not_exist.txt'.format(result)
    with file(disappearing_file, 'w') as file_to_make_dissapear:
        file_to_make_dissapear.write('make me disappear')
    assert os.listdir(result)[0] == 'i_should_not_exist.txt'
    result2 = test_helpers.placebos_path(test_file, 'some_test', mode='record')
    assert len(os.listdir(result2)) == 0

