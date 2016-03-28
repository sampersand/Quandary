__toimport__ = ('Obj', 'NullObj', 'NoneObj')
def _import_file(_obj, _path):
    return __import__(_path + '.' + _obj, fromlist = _obj.lower()).__getattribute__(_obj.lower())

def _import(_obj):
    return __import__(__package__, fromlist = _obj).__getattribute__(_obj)

if '__init__' not in __name__: #aka, it's not being imported from NoneObj or the ilk
    import os
    for _dir in os.walk('./' + __package__.replace('.', '/')):
        if _dir[0] != './objs':
            continue
        if '__init__.py' in _dir[2]:
            module = __import__(_dir[0].replace('./','').replace('/', '.') + '.__init__', fromlist = '__toimport__')
            if __debug__:
                assert '__toimport__' in dir(module), "Error! '{}/__init__.py' doesn't have an import list!".format(_dir[0])
            for _obj in module.__toimport__:
                print([x for x in locals().keys() if x[0] != '_'], 'b4')
                locals()[_obj.lower()] = _import_file(_obj, module.__package__)
                print([x for x in locals().keys() if x[0] != '_'], 'l8')
    del os, _dir, module, _obj
    __all__ = [o for o in locals().keys() if 'bj' in o]