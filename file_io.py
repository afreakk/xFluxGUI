import os
HOME = os.path.expanduser("~")
FLUXGUIPATH = HOME+'/.xfluxgui/'
SETTINGFILE = FLUXGUIPATH+'settings.ini'

def set_default_values():
    s = Saver()
    s.save(58, 10, 3400)

class Saver(object):
    def __init__(self):
        if not os.path.exists(FLUXGUIPATH):
            os.makedirs(FLUXGUIPATH)
    def save(self, lng, lat, tmp):
        int(lng), int(lat), int(tmp) #check if valid intz
        f = open(SETTINGFILE , 'w+')
        f.write('long=%s|'% lng)
        f.write('lat=%s|'% lat)
        f.write('tmp=%s'% tmp)
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
            int(lng), int(lat), int(tmp) #check if valid intz
        except Exception as e:
            set_default_values()
            return self.get_values()
        return lng, lat, tmp
