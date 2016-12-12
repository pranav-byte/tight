import tight.providers.aws.controllers.lambda_proxy_event as lambda_proxy

@lambda_proxy.get
def get_method(*args, **kwargs):
    return 'GET'