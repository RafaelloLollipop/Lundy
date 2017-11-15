from boltons.funcutils import wraps

from datasets import Method, LundyMethod


class Lundy:
    @staticmethod
    def collector(*spec_args, **spec_kwargs):
        def collector_decorator(func):
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                loc = locals()
                result = func(*args, **kwargs)
                lundy_method = LundyMethod(loc['func'].__name__)
                lundy_method.scan(func)
                method_hash = lundy_method.hash
                m = Method(name=loc['func'].__name__,
                       args=args,
                       kwargs=kwargs,
                       result=result,
                       hash=method_hash,
                )
                m.save()
                return result
            return func_wrapper
        return collector_decorator
