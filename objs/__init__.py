__toimport__ = ('obj', 'nullobj', 'varobj', 'pyobj', 'strobj', 
                ('numbers', 'numobj', 'intobj', 'floatobj', 'complexobj', 'boolobj'),
                ('functions', 'funcobj', 'ibfuncobj', 'operobj'))
if '__init__' not in __name__:
    import re, os
    def _import(_objs_list, package):
        for _obj in _objs_list:
            if isinstance(_obj, str):
                yield (_obj, __import__(package + _obj, fromlist = _obj).__getattribute__(_obj))
            if isinstance(_obj, tuple):
                for x in _import(_obj[1:], package + _obj[0] + '.'):
                    yield x
    for _obj_name, _obj_type in _import(__toimport__, __package__ and __package__ + '.' or ''):
        locals()[_obj_name] = _obj_type
    # locals().update()
    del _import, _obj_name, _obj_type

    _regexes = {re.compile(o._regex):o for o in locals().values() if hasattr(o, '_regex')}
    #     del os, _dir, module, _obj, re
    __all__ = [o for o in locals().keys() if 'obj' in o]

    def getobj(node: 'node', data: (str, None)) -> obj:
        if data == None:
            return varobj()
        if data == '':
            return nullobj()
        if data in node.consts.opers:
            return node.consts.opers[data]['obj']()
        for k, v in _regexes.items():
            if k.fullmatch(data):
                return v()
        return varobj()
    # g=[__import__('random').randint(1,100)]
    # while g.append(int(input()))or g[-1]!=g[0]:print(g[-1]<g[0],len(g))