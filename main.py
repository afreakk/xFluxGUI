from gi.repository import Gtk, GObject
import long_lat_getter
import file_io
import xflux_control

class Console(object):
    def __init__(self, textview):
        self.textbuffer = textview.get_buffer()
        self.append_txt("\n\n--xfluxgui--")
    def append_txt(self, txt):
        self.textbuffer.insert_at_cursor(txt)
    def clear_txt(self):
        self.textbuffer.set_text("")

def get_labeled_entry(labelName):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        label = Gtk.Label(labelName)
        hbox.pack_start(label, False, False, 10)

        entry = Gtk.Entry()
        hbox.pack_start(entry, True, True, 0)
        return hbox, entry

class EntryWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="xFluxGUI")
        self.saver = file_io.Saver()
        self.loader = file_io.Loader()
        self.flux = xflux_control.Xflux()
        self.set_size_request(320, 320)
        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        hbox, self.entry_loc = get_labeled_entry("Location")
        self.entry_loc.set_text("Picadilly circus")
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Longitude latitude from location")
        button.connect("clicked", self.lat_lng_from_location)
        vbox.pack_start(button, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(True)
        self.console = Console(self.textview)
        vbox.pack_start(self.textview, True, True, 0)
        
        hbox, self.entry_lng = get_labeled_entry("Longitude")
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_lat = get_labeled_entry("Latitude")
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_temp = get_labeled_entry("Color temperature (default 3400)")
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Save and refresh xflux")
        button.connect("clicked", self.save_and_update)
        vbox.pack_start(button, True, True, 0)

    def set_loaded_values(self):
        try:
            self.console.clear_txt()
            lng, lat, tmp = self.loader.get_values()
            int(lat), int(lat), int(tmp)
            self.entry_lng.set_text(lng)
            self.entry_lat.set_text(lat)
            self.entry_temp.set_text(tmp)
        except Exception as l:
            self.console.append_txt(l.__str__())

    def save_and_update(self, button):
        try:
            self.console.clear_txt()
            lng = self.entry_lng.get_text()
            lat = self.entry_lat.get_text()
            tmp = self.entry_temp.get_text()
            self.saver.save(lng, lat, tmp)
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
            self.console.append_txt("Successfully got lat lng from:\n" + locstr)
        except Exception as l:
            self.console.append_txt(l.__str__())

def main():
    win = EntryWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    win.set_loaded_values()
    Gtk.main()

if __name__ == "__main__":
    main()
