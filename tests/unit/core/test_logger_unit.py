import tight.core.logger as logger

def test_no_boom():
    assert True, 'Module can be imported.'

def test_logger_info():
    test_message = 'test message'
    def info_spy(message):
        assert message == 'test message', 'The message is logged'
    setattr(logger.logger, 'info', info_spy)
    logger.info(message=test_message)