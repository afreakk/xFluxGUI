import os
HOME = os.path.expanduser("~")
FLUXGUIPATH = HOME+'/.xfluxgui/'
SETTINGFILE = FLUXGUIPATH+'settings.ini'

def set_default_values():
    s = Saver()
    s.save(58, 10, 3400, "picadilly circus")

class Saver(object):
    def __init__(self):
        if not os.path.exists(FLUXGUIPATH):
            os.makedirs(FLUXGUIPATH)
    def save(self, lng, lat, tmp, loc):
        float(lng), float(lat), float(tmp) #check if valid floatz
        f = open(SETTINGFILE , 'w+')
        f.write('long=%s|'% lng)
        f.write('lat=%s|'% lat)
        f.write('tmp=%s|'% tmp)
        f.write('loc=%s'% loc)
        f.close()

class Loader(object):
    def __init__(self):
        pass
    def get_values(self):
        try:
            f = open(SETTINGFILE, 'r+')
            data = f.read().split('|')
            f.close()
            values = [x.split('=')[1] for x in data]
            lng = values[0]
            lat = values[1]
            tmp = values[2]
            loc = values[3]
            float(lng), float(lat), float(tmp) #check if valid floatz
        except Exception as e:
            print e
            set_default_values()
            return self.get_values()
        return lng, lat, tmp, loc
