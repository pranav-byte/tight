import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def info(*args, **kwargs):
    """
    Log a message using the system logger.

    :param args:
    :param kwargs:
    :return: None
    """
    message = kwargs.pop('message')
    logger.info(message)