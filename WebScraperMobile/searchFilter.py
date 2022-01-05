"""several filters each returning a specific string"""
class SearchFilter:
    def __init__(self):
        pass

    """must be placed in front of isSearchRequest"""
    def fltr_damage(self):
        return 'dam=0&'

    """must be placed in front of isSearchRequest"""
    def fltr_reg(self, start: int=None, end: int=None):
        if start and end:
            return "fr={}%3A{}&".format(str(start), str(end))
        elif start:
            return "fr={}%3A&".format(str(start))
        elif end:
            return "fr=%3A{}&".format(str(end))

    """must be placed in front of isSearchRequest"""
    def fltr_gas(self, gas=True):
        if gas:
            return "ft=PETROL&"
        else:
            return "ft=DIESEL&"

    """must be placed after isSearchRequest"""
    def fltr_mil(self, start: int=None, end: int=None):
        if start and end:
            return "ml={}%3A{}&".format(str(start),str(end))
        elif start:
            return "ml={}%3A&".format(str(start))
        elif end:
            return "ml=%3A{}&".format(str(end))

    """must be placed after isSearchRequest"""
    def fltr_pw(self, start: int=None, end: int=None):
        if start and end:
            return "pw={}%3A{}&".format(str(start),str(end))
        elif start:
            return "pw={}%3AKW&".format(str(start))
        elif end:
            return "pw=KW%3A{}&".format(str(end))

    """must be placed after isSearchRequest, option: 'automatic'"""
    def fltr_trans(self, trans="manual"):
        if "automatic" in trans:
            return "tr=AUTOMATIC_GEAR&"
        else:
            return "tr=MANUAL_GEAR&"

    """must be placed after isSearchRequest, param: start(int), end(int)"""
    def fltr_price(self, start: int=None, end: int=None):
        if start and end:
            return "p={}%3A{}&".format(str(start),str(end))
        elif start:
            return "p={}%3A&".format(str(start))
        elif end:
            return "p=%3A{}&".format(str(end))
