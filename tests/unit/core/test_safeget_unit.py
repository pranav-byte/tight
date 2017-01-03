import tight.core.safeget as safeget

def test_no_boom():
    assert True, 'Module can be imported.'

def test_safeget():
    some_dict = {
        'a_key': 'a value'
    }

    success = safeget.safeget(some_dict, 'a_key')
    assert success == 'a value', 'An existing key is retrieved.'
    failure = safeget.safeget(some_dict, 'a_non_existent_key')
    assert failure == None