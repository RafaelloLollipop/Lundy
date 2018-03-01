import datetime
import inspect
import os

from boltons.funcutils import wraps

from datasets import LundyMethod, ResultPackage


class Lundy:
    """ Main class to store information about runs
    Can be used on method or on class (to decorate all class methods)

    Usage:

    @Lundy.collector()
    def method1:
        pass

    @Lundy.collector()
    class class1():
        pass
    """
    @staticmethod
    def collector(*spec_args, **spec_kwargs):
        config = spec_kwargs.get('config')
        if config:
            os.environ['LUNNICONFIG'] = config
        def collector_decorator(obj):
            if inspect.isfunction(obj):
                return method_wrapper(obj)
            elif inspect.isclass(obj):
                for method in obj.__dict__:
                    method_object = getattr(obj, method)
                    if inspect.ismethod(method_object):
                        setattr(obj, method, method_wrapper(method_object))
                return obj
        return collector_decorator


def method_wrapper(obj):
    @wraps(obj)
    def func_wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        # if getattr(obj, '_lundy_run_hash', False):
        #     # TODO
        #     print(obj._lundy_run_hash)
        # else:
        #     setattr(obj, '_lundy_run_hash', 'timehash')
        result = obj(*args, **kwargs)
        duration = (datetime.datetime.now() - start_time).total_seconds()
        lundy_method = LundyMethod(obj.__name__)
        lundy_method.scan(obj)
        method_hash = lundy_method.hash
        m = ResultPackage(name=obj.__name__,
                   args=args,
                   kwargs=kwargs,
                   result=result,
                   hash=method_hash,
                   start_time=start_time,
                   duration=duration
                   )
        m.save()
        return result

    return func_wrapper