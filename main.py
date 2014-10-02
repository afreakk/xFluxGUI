from gi.repository import Gtk, GObject
import os
import subprocess
HOME = os.path.expanduser("~")
FLUXGUIPATH = HOME+'/.fluxgui/'
SETTINGFILE = FLUXGUIPATH+'settings.ini'
class Xflux(object):
    def __init__(self):
        pass
    def update(self, lo, la, te):
        killFlux = "kill -9 `pgrep xflux`"
        bashCommand = "xflux -l %s -g %s -k %s" % (lo, la, te)
        process = subprocess.Popen(killFlux.split(), stdout=subprocess.PIPE)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

class Saver(object):
    def __init__(self):
        if not os.path.exists(FLUXGUIPATH):
            os.makedirs(FLUXGUIPATH)
    def save(self, lo, la, te):
        f = open(SETTINGFILE , 'w+')
        f.write('long=%s\n'% lo)
        f.write('lat=%s\n'% la)
        f.write('temp=%s\n'% te)

class Loader(object):
    def __init__(self):
        pass
    def get_values(self):
        f = open(SETTINGFILE, 'r+')
        tmp = [x.split('=')[1] for x in f.read().split()]
        if len(tmp) == 3:
            longitude = tmp[0]
            latitude = tmp[1]
            temp = tmp[2]
        else:
            s = Saver()
            s.save(58, 10, 3400)
            self.__init__()
        return longitude, latitude, temp

class EntryWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="FluxGUI")
        self.saver = Saver()
        self.loader = Loader()
        self.flux = Xflux()
        lo, la, te = self.loader.get_values()
        self.set_size_request(200, 100)
        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry_long = Gtk.Entry()
        self.entry_long.set_text(lo)
        vbox.pack_start(self.entry_long, True, True, 0)


        self.entry_lat = Gtk.Entry()
        self.entry_lat.set_text(la)
        vbox.pack_start(self.entry_lat, True, True, 0)

        self.entry_temp = Gtk.Entry()
        self.entry_temp.set_text(te)
        vbox.pack_start(self.entry_temp, True, True, 0)

        button = Gtk.Button("Save and update")
        button.connect("clicked", self.save_and_update)
        vbox.pack_start(button, True, True, 0)

    def save_and_update(self, button):
        print button
        longitude = self.entry_long.get_text()
        latitude = self.entry_lat.get_text()
        colortemp = self.entry_temp.get_text()
        self.saver.save(longitude, latitude, colortemp)
        self.flux.update(longitude, latitude, colortemp)

x = Xflux()
win = EntryWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
