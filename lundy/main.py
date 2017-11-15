import datetime
import inspect

from boltons.funcutils import wraps

from datasets import Method, LundyMethod


class Lundy:
    @staticmethod
    def collector(*spec_args, **spec_kwargs):
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
        result = obj(*args, **kwargs)
        duration = (datetime.datetime.now() - start_time).total_seconds()
        lundy_method = LundyMethod(obj.__name__)
        lundy_method.scan(obj)
        method_hash = lundy_method.hash
        m = Method(name=obj.__name__,
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