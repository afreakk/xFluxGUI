import os
HOME = os.path.expanduser("~")
FLUXGUIPATH = HOME+'/.fluxgui/'
SETTINGFILE = FLUXGUIPATH+'settings.ini'

def set_default_values():
    s = Saver()
    s.save(58, 10, 3400)

class Saver(object):
    def __init__(self):
        if not os.path.exists(FLUXGUIPATH):
            os.makedirs(FLUXGUIPATH)
    def save(self, lo, la, te):
        f = open(SETTINGFILE , 'w+')
        f.write('long=%s|'% lo)
        f.write('lat=%s|'% la)
        f.write('temp=%s'% te)
        f.close()

class Loader(object):
    def __init__(self):
        pass
    def get_values(self):
        try:
            f = open(SETTINGFILE, 'r+')
            data = f.read().split('|')
            values = [x.split('=')[1] for x in data]
        except:
            set_default_values()
            return self.get_values()
        finally:
            f.close()
        if len(values) == 3:
            longitude = values[0]
            latitude = values[1]
            temp = values[2]
        else:
            set_default_values()
            return self.get_values()
        return longitude, latitude, temp
