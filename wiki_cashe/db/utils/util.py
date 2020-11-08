from distutils.util import strtobool
class ConvertData:
    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            function_class = self.function.__qualname__.split('.')[0].upper()
            function_name = self.function.__name__.lower()
            return self.w_function(function_class, function_name, self.function,  instance, *args, **kwargs)  # note, self here is the descriptor object
        return wrapper

    @staticmethod
    async def w_function(function_class, function_name, function, instance, *args, **kwargs):
        result = None
        if function_class == 'REDIS':
            if function_name == 'get_value':
                result = await function(instance, *args, **kwargs)
                _success= strtobool(str(result.get('success', 'False')))
                result.update({'success':True if _success else False})
            elif function_name == 'set_value':
                kwargs['value'].update({'success':'True' if kwargs['value']['success'] else 'False'})
                await function(instance, *args, **kwargs)
        elif function_class == 'POSTGRESQL':
            if function_name == 'get_value':
                result = await function(instance, *args, **kwargs)
                _success = strtobool(str(result.get('success', 'False')))
                result.update({'success':True if _success else False})
            elif function_name == 'set_value':
                await function(instance, *args, **kwargs)
        return result