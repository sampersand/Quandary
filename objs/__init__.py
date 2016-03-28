__toimport__ = ('obj', 'nullobj', 'noneobj')
def _import_file(_obj, _path):
    return 

def _import(_obj):
    return __import__(__package__, fromlist = _obj).__getattribute__(_obj)

if '__init__' not in __name__: #aka, it's not being imported from NoneObj or the ilk
    import os
    for _dir in os.walk('./' + __package__.replace('.', '/')):
        if '__init__.py' in _dir[2]:
            module = __import__(_dir[0].replace('./','').replace('/', '.') + '.__init__', fromlist = '__toimport__')
            if __debug__:
                assert '__toimport__' in dir(module),\
                    "Error! '{}/__init__.py' doesn't have an import list!".format(_dir[0])
            for _obj in module.__toimport__:
                locals()[_obj.lower()] = __import__(module.__package__ + '.' + _obj, fromlist = _obj).\
                                         __getattribute__(_obj.lower())
    del os, _dir, module, _obj
    __all__ = [o for o in locals().keys() if 'obj' in o]
    