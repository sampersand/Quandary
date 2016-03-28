from objs import numobj
class floatobj(numobj):
    """ A floating poitn number. """
    _regex = r'(\d+)?\.(?(1)\d*|\d+)[fF]?'
