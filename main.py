#!/usr/bin/env python
from gi.repository import Gtk, GObject
from utils import long_lat_getter
from utils import file_io
from utils import xflux_control
from utils import console

class FluxGuiWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="xFluxGUI")
        self.init_core()
        self.init_gui()
        self.connect_events()

    def init_core(self):
        self.saver = file_io.Saver()
        self.loader = file_io.Loader()
        self.flux = xflux_control.Xflux()
        self.set_size_request(320, 320)
        self.timeout_id = None

    def connect_events(self):
        self.restart_btn.connect("clicked", self.save_and_update)
        self.get_coord_btn.connect("clicked", self.lat_lng_from_location)
        self.kill_flux_btn.connect("clicked", self.kill_flux)

    def init_gui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        hbox, self.entry_loc = get_labeled_entry("Location")
        vbox.pack_start(hbox, True, True, 0)

        self.get_coord_btn = Gtk.Button("Longitude latitude from location")
        vbox.pack_start(self.get_coord_btn, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(True)
        self.console = console.Console(self.textview)
        vbox.pack_start(self.textview, True, True, 0)
        
        hbox, self.entry_lng = get_labeled_entry("Longitude")
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_lat = get_labeled_entry("Latitude")
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_temp = get_labeled_entry("Color temperature (default 3400)")
        vbox.pack_start(hbox, True, True, 0)

        self.restart_btn = Gtk.Button("Save and restart xflux")
        vbox.pack_start(self.restart_btn, True, True, 0)

        self.kill_flux_btn = Gtk.Button("Kill xflux")
        vbox.pack_start(self.kill_flux_btn, True, True, 0)

    def set_loaded_values(self):
        try:
            self.console.clear_txt()
            lng, lat, tmp, loc = self.loader.get_values()
            float(lat), float(lat), float(tmp)
            self.entry_lng.set_text(lng)
            self.entry_lat.set_text(lat)
            self.entry_temp.set_text(tmp)
            self.entry_loc.set_text(loc)
        except Exception as l:
            self.console.append_txt(l.__str__())

# ---- callbacks-->
    def kill_flux(self, button):
        try:
            pids = self.flux.kill_flux()
            self.console.append_txt("Successfully killed flux with pid: " + pids)
        except Exception as l:
            self.console.append_txt(l.__str__())

    def save_and_update(self, button):
        try:
            self.console.clear_txt()
            lng = self.entry_lng.get_text()
            lat = self.entry_lat.get_text()
            tmp = self.entry_temp.get_text()
            loc = self.entry_loc.get_text()
            self.saver.save(lng, lat, tmp, loc)
            self.flux.update(lng, lat, tmp, self.console)
        except Exception as l:
            self.console.append_txt(l.__str__())

    def lat_lng_from_location(self, button):
        try:
            self.console.clear_txt()
            l = long_lat_getter.LongLatGetter()
            lat, lng, locstr = l.get_lng_lat(self.entry_loc.get_text())
            self.entry_lat.set_text(str(lat))
            self.entry_lng.set_text(str(lng))
            self.console.append_txt("Successfully got coordinates from:\n" + locstr + "\nlng: %.2f lat: %.2f."%(lng,lat))
        except Exception as l:
            self.console.append_txt(l.__str__())
# ---- end-callbacks<--

def get_labeled_entry(labelName):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        label = Gtk.Label(labelName)
        hbox.pack_start(label, False, False, 10)

        entry = Gtk.Entry()
        hbox.pack_start(entry, True, True, 0)
        return hbox, entry

def main():
    win = FluxGuiWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    win.set_loaded_values()
    Gtk.main()

if __name__ == "__main__":
    main()
