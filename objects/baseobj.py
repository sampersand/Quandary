class _property():
  def __init__(self, pobject):
    self._obj = pobject
  def __getattr__(self, attr):
    return self._obj._qfuncs()[attr]()

class baseobj():
  """ The object that everything else extends from """

  def __init__(self, data:object = None) -> None:
    self._data = data

  @property
  def data(self):
    return self._data
  
  def __str__(self) -> str:
    return '{}({})'.format(type(self).__qualname__, '' if self.data == None else str(self.data))

  def __getattr__(self, attr):
    if attr != 'qf':
      return super().__getattr__(attr)
    return _property(self)

  def _qfuncs(self):
    pass

