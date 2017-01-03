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