import sys, inspect
from typing import Callable
def verify():
    back = inspect.currentframe().f_back
    print('annotations' in str(inspect.getmembers(back)))
    vals = inspect.getfullargspec(back)
    print(inspect.stack()[1].frame)
    return vals
thisfunc = lambda: sys._getframe().f_globals#[sys._getframe().f_code.co_name]


def checkparams(func: Callable, params: dict):
    annotations = func.__annotations__
    for param in params:
        if param not in annotations or (type(params[param]).__qualname__ != str(annotations[param]) and
                                        type(params[param]).__qualname__ != annotations[param].__qualname__):
            return False
    return True
class c():
    def g(a: str, b:int = 1):
        print(*dir(inspect), sep = '\n')
        print('\n',verify(),sep='')
    def f(a = 1):
    # def f(obj, *, a = 1):
        c.g(1)
c.f(3)