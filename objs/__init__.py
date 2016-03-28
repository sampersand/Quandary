import re, os
__toimport__ = ('obj', 'nullobj', 'varobj', 'pyobj')

def _import(_obj: str) -> 'obj':
    return __import__(__package__, fromlist = _obj).__getattribute__(_obj)

if '__init__' not in __name__: #aka, it's not being imported from NoneObj or the ilk
    for _dir in os.walk('./' + __package__.replace('.', '/')):
        if '__init__.py' in _dir[2]:
            module = __import__(_dir[0].replace('./','').replace('/', '.') + '.__init__', fromlist = '__toimport__')
            if __debug__:
                assert '__toimport__' in dir(module),\
                    "Error! '{}/__init__.py' doesn't have an import list!".format(_dir[0])
            for _obj in module.__toimport__:
                locals()[_obj.lower()] = __import__(module.__package__ + '.' + _obj, fromlist = _obj).\
                                         __getattribute__(_obj.lower())
    _regexes = {re.compile(o._regex):o for o in locals().values() if hasattr(o, '_regex')}
    del os, _dir, module, _obj, re
    __all__ = [o for o in locals().keys() if 'obj' in o]

    def getobj(node: 'node', data: (str, None)) -> obj:
        if data == None:
            return varobj()
        if data == '':
            return nullobj()
        if data in node.consts.opers:
            return node.consts.opers[data][0]()
        for k, v in _regexes.items():
            if k.match(data):
                return v()
        return varobj()
# g=[__import__('random').randint(1,100)]
# while g.append(int(input()))or g[-1]!=g[0]:print(g[-1]<g[0],len(g))