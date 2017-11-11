import os
from functools import wraps
from datasets import Method, LundyMethod, LundyProject


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
                return result
            return func_wrapper
        return collector_decorator



dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(dir_path, 'test', 'sample_project_dir')
project = LundyProject("Lundy")
project.scan(project_dir)
print("")
print(project.__dict__)