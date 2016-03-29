from objs import obj, pyobj
class strobj(pyobj, obj):
    """ A String object. """
    _regex = r'["\'].*["\']'
    _pyobj = str
    _pyobj_rank = 4
    # def __add__(self, *args, passa):
        # if args[0][-1] in args[0].control
