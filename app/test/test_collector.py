from app.main import Lundy


@Lundy.collector("D")
def sample_method1(var, var2, var3='raf'):
    return var + var2


print(sample_method1(1, 2, var3='d'))
