
from app.main import Lunni

@Lunni.collector("D")
def sample_method1(var, var2):
    return var + var2



print(sample_method1(1,2))