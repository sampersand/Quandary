__toimport__ = ('Obj', 'NullObj', 'NoneObj')

# __package__ = ___package____ + '.'; __package__ = __package__[:__package__.find('.')]
def _import_file(_obj, _path = __package__):
    return __import__(_path + '.' + _obj, fromlist = _obj.lower()).__getattribute__(_obj.lower())
def _import(_obj):
    # return locals()[_obj]
    return __import__(__package__, fromlist = _obj).__getattribute__(_obj)

if '__init__' not in __name__:
    import os
    for _dir in os.walk('./' + __package__.replace('.', '/')):
        if '__init__.py' in _dir[2]:
            i = __import__(_dir[0].replace('./','').replace('/', '.') + '.__init__', fromlist = '__toimport__')
            for _objtoimport in zip((o for o in i.__toimport__), [i.__package__] * len(i.__toimport__)):
                locals()[_objtoimport[0].lower()] = _import_file(*_objtoimport)
                print(locals().keys())






    # locals()[file.lower()] = importobj(locals()__import__(package + file, fromlist = file.lower())
# # from objs.NullObj import nullobj
# # from objs.NoneObj import noneobj
# # from objs.Functions.FuncObj import funcobj
# # from objs.Functions.IBFuncObj import ibfuncobj
# # from objs.Functions.OperObj import operobj
# # from objs.Functions.OperObj import operobj

# from typing import Union
# import re
# import os
# from objs.Obj import obj
# for _dir in os.walk('./objs'):
#     files = _dir[2]
#     for file in files:
#         if len(file) > 2 and file[-3:] == '.py' and file != '__init__.py':
#             print(file, files)
#             __import__(_dir[0][2:] + '.' + file)
# regexes = {o._regex:o for o in locals().values() if hasattr(o, '_regex')}
# def getobj(node: 'node', data: Union[str, None]) -> obj:
#     if data == None:
#         return noneobj
#     if data in node.consts.operators:
#         return node.consts.operators[data]
