import os, importlib, traceback, sys
from functools import partial
from tight.core.logger import info

def run():
    try:
        info(message='CREATING APP')
        create(sys.modules['app_index'])
    except Exception as e:
        info(message='UNABLE TO RUN')
        info(message=e)
        traceback.print_exc()


def create(current_module):
    """ Attach functions to the app entry module.

    Introspect the application function root and create function attributes on the provided
    module that map to each application controller. An application controller
    is defined as any directory in the app root that contains a `handler.py` file.
    The name of the controller is the enclosing directory.

    Given the following app structure:

    app_index.py
    app/
        functions/
            controller_a/
                handler.py
            controller_b/
                handler.py
            not_a_controller/
                some_other_python.py

    The controller names collected would be:

    `controller_a` and `controller_b`

    Notice that `not_a_controller` is omitted because there is no `handler.py` file in the directory.

    Assuming that `app_index.py` is the module from which `create` is called, the result would  be that
    `app_index.py` will behave as if it had been statically defined as:

    def controller_a(controller_module_path, controller_name, event, context):
        controller_module_path # 'app.functions.controller_a.handler'
        controller_name # controller_a
        callback = importlib.import_module(controller_module_path, 'handler')
        return callback.handler(event, context, **kwargs)


    def controller_b(controller_module_path, controller_name, event, context):
        controller_module_path # 'app.functions.controller_b.handler'
        controller_name # controller_b
        callback = importlib.import_module(controller_module_path, 'handler')
        return callback.handler(event, context, **kwargs)


    This means that the handler value provided to lambda can follow the format:

    'app_index.controller_a'
    'app_index.controller_b'

    So long as `app.functions.controller_a.handler` and `app.functions.controller_b.handler` define
    functions that are decorated by `tight.providers.aws.controllers.lambda_proxy_event` the call to
    `app_index.controller_a` or `app_index.controller_b` will in turn call the correct handler for the
    request method by mapping `event['httpMethod']` to the correct module function.

    """
    controllers = collect_controllers()
    for item in controllers:
        name, controller_module_path = item.popitem()
        def function(*args, **kwargs):
            controller_module_path = args[0]
            func_args = args[1:4]
            callback = importlib.import_module(controller_module_path, 'handler')
            return callback.handler(*func_args, **kwargs)
        bound_function = partial(function, *(controller_module_path, name))
        function.__name__ = name + '_module'
        setattr(current_module, name, bound_function)

def collect_controllers():
    """" Inspect the application directory structure and discover controller modules.

    Given the following directory structure:

    app/
        functions/
            controller_a/

    :rtype: list
    :return: A list of controller name to module path mappings.
    """
    app_root = os.environ.get('TIGHT.APP_ROOT', 'app/functions')
    controllers = []
    for dirName, subdirList, fileList in os.walk(app_root):
        if ('handler.py' in fileList):
            controller_module_path = (dirName + '/handler').replace('/', '.')
            controller_name = controller_module_path.split('.')[-2]
            callback = {}
            callback[controller_name] = controller_module_path
            controllers.append(callback)
    return controllers