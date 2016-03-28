_super = 'FuncObj'; _init_file = __import__(__package__)
class operobj(_init_file._import(_super, _init_file.__package__)):
    """ An operator. """
    def evalobj(*args, **kwargs):
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
        print(args)