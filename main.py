class qproperty():
  def __init__(self, pobj, pfunc):
    self.obj = pobj
    self.func = pfunc

  def __getattr__(self, attr):
    call = self.func(self.obj)[attr]
    if 'return' in call.__annotations__ and call.__annotations__['return'] == qproperty:
      return qproperty(self.obj, call)
    return call()

class foo():

  def __init__(self, px): 
    self.x = px

  def __getattr__(self, attr):
    if attr != '_':
      return super().__getattr__(attr)
    return qproperty(self, foo._funcs)
  
  def _funcs(self):
    def bar1(self) -> qproperty:
      def func1():
        return self.x
      return locals()
    def func2():
      return self.x ** 2
    return locals()
f = foo(9)
print(f._.bar1.func1, f._.func2)
















# from types import MethodType, FunctionType
# import types
# class qproperty():
#   def __init__(self, pfunc, pobj = None):
#     self.func = pfunc
#     self.obj = pobj

#   def __getattr__(self, attr):
#     callfunc = isinstance(self.func, MethodType) and self.func()[attr] or self.func(self.obj)[attr]
#     return isinstance(callfunc, MethodType) and callfunc() or callfunc(self.obj)

# class foo():

#   def __init__(self, px): 
#     self.x = px

#   def __getattr__(self, attr):
#     if attr != '_':
#       return super().__getattr__(attr)
#     return qproperty(self._funcs)
  
#   def _funcs(self):
#     def bar1(self):
#       def func1():
#         return self.x
#       return locals()
#     def func2():
#       return self.x ** 2
#     return locals()
# f = foo(9)
# print(f._.bar1.func1, f._.func2)