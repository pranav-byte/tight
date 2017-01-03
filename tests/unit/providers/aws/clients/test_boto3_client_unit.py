from tight.providers.aws.clients import boto3_client

def test_no_boom():
    assert True, 'Client can be imported.'


def test_session():
    session = boto3_client.session()
    session_2 = boto3_client.session()
    assert session == session_2, 'The session returned from session() is always the same'