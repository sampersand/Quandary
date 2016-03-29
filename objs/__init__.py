__toimport__ = ('obj', 'nullobj', 'varobj', 'pyobj', 'strobj', 
                ('numbers', 'numobj', 'floatobj', 'intobj', 'complexobj', 'boolobj'),
                ('functions', 'funcobj', 'ibfuncobj', 'operobj'))
if '__init__' not in __name__:
    import re, os
    __all__ = []
    def _import(_objs_list, package):
        for _obj in _objs_list:
            if isinstance(_obj, str):
                yield (_obj, __import__(package + _obj, fromlist = _obj).__getattribute__(_obj))
            if isinstance(_obj, tuple):
                for x in _import(_obj[1:], package + _obj[0] + '.'):
                    yield x
    for _obj_name, _obj_type in _import(__toimport__, __package__ and __package__ + '.' or ''):
        locals()[_obj_name] = _obj_type
        __all__.append(_obj_name)

    # _regexes = {re.compile(o._regex):o for o in locals().values() if hasattr(o, '_regex')}

    def getobj(node: 'node', data: (str, None)) -> obj:
        if data == None:
            return data, varobj()
        for cobj in __all__:
            ret = globals()[cobj].fromstr(data, node.consts)
            if ret != None:
                return ret
        # if data == '':
        #     return data, nullobj()
        # if data in node.consts.opers:
        #     return node.consts.opers[data]['obj'].fromstr(data)
        # for k, v in _regexes.items():
        #     if k.fullmatch(data):
        #         return v.fromstr(data)
        return data, varobj()
    # g=[__import__('random').randint(1,100)]
    # while g.append(int(input()))or g[-1]!=g[0]:print(g[-1]<g[0],len(g))

























