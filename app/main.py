from functools import wraps

from datasets import Method


# Other metadata to collect
# for method_name in dir(func):
#     method = getattr(func, method_name)
#     try:
#         print(method())
#     except:
#         print(method)

class Lunni:
    @staticmethod
    def collector(*spec_args, **spec_kwargs):
        def collector_decorator(func):
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                loc = locals()
                result = func(*args, **kwargs)
                Method(name=loc['func'].__name__,
                       args=args,
                       kwargs=kwargs,
                       result=result
                ).save()
                return result
            return func_wrapper
        return collector_decorator

#
x = 10
# for a in dir():
#     print(a)

# for value in vars().values():
#   print(value)

# print(globals())

#print(locals())


# import pdb
#
# def f(n):
#     for i in range(n):
#         j = i * n
#         print(i, j)
#     return
#
# if __name__ == '__main__':
#     pdb.set_trace()
#     f(5)


