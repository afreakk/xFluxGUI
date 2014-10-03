from gi.repository import Gtk, GObject
import os
import subprocess
import long_lat_getter

HOME = os.path.expanduser("~")
FLUXGUIPATH = HOME+'/.fluxgui/'
SETTINGFILE = FLUXGUIPATH+'settings.ini'

class Xflux(object):
    def __init__(self):
        pass
    def update(self, lo, la, te):
        try:
            while True:
                getFluxPid = "pgrep xflux"
                fluxPID = subprocess.check_output(getFluxPid.split())
                killFlux = "kill -9 "+fluxPID
                subprocess.call(killFlux.split())
        except subprocess.CalledProcessError:
            pass
        runFlux = "xflux -l %s -g %s -k %s" % (lo, la, te)
        subprocess.call(runFlux.split())

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
        Gtk.Window.__init__(self, title="xFluxGUI")
        self.saver = Saver()
        self.loader = Loader()
        self.flux = Xflux()
        lo, la, te = self.loader.get_values()
        self.set_size_request(200, 100)
        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry_loc = Gtk.Entry()
        self.entry_loc.set_text("Location")
        vbox.pack_start(self.entry_loc, True, True, 0)

        button = Gtk.Button("Longitude latitude from location")
        button.connect("clicked", self.lat_lng_from_location)
        vbox.pack_start(button, True, True, 0)

        label = Gtk.Label("Latitude")
        vbox.pack_start(label, True, True, 0)

        self.entry_lat = Gtk.Entry()
        self.entry_lat.set_text(la)
        vbox.pack_start(self.entry_lat, True, True, 0)

        label = Gtk.Label("Longitude")
        vbox.pack_start(label, True, True, 0)

        self.entry_lng = Gtk.Entry()
        self.entry_lng.set_text(lo)
        vbox.pack_start(self.entry_lng, True, True, 0)

        label = Gtk.Label("Color temperature")
        vbox.pack_start(label, True, True, 0)

        self.entry_temp = Gtk.Entry()
        self.entry_temp.set_text(te)
        vbox.pack_start(self.entry_temp, True, True, 0)

        button = Gtk.Button("Save and update")
        button.connect("clicked", self.save_and_update)
        vbox.pack_start(button, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(True)
        self.textbuffer = self.textview.get_buffer()
        vbox.pack_start(self.textview, True, True, 0)

    def save_and_update(self, button):
        longitude = self.entry_lng.get_text()
        latitude = self.entry_lat.get_text()
        colortemp = self.entry_temp.get_text()
        self.saver.save(longitude, latitude, colortemp)
        self.flux.update(longitude, latitude, colortemp)
    def get_buffer_text(self):
        return self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), True)
    def lat_lng_from_location(self, button):
        l = long_lat_getter.LongLatGetter()
        try:
            lat, lng = l.get_lng_lat(self.entry_loc.get_text())
        except long_lat_getter.Rxpt as r:
            ermsg = ""
            for x in r.args:
                ermsg += x
            self.textbuffer.set_text(ermsg)
            return
        self.entry_lat.set_text(str(lat))
        self.entry_lng.set_text(str(lng))

def main():
    x = Xflux()
    win = EntryWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
