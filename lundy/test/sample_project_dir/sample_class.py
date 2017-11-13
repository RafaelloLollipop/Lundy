from lundy.main import Lundy


class SampleClass:
    def __init__(self, var2, var3):
        self.var1 = 'var1'
        self.var2 = var2
        self.var3 = var3

    @Lundy.collector()
    def sample_method(self):
        pass

    @Lundy.collector()
    def sample_method_with_args(self, arg1, arg2):
        return arg1, arg2

    @Lundy.collector()
    def sample_method_with_kwargs(self, arg3=None, arg4=4):
        return arg3, arg4

    @Lundy.collector()
    def sample_method_with_args_and_kwargs(self, arg5, arg6, arg7=None, arg8=4):
        return arg5, arg8

class SampleClass2:
    pass