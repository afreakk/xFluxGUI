from gi.repository import Gtk, GObject
import long_lat_getter
import file_io
import xflux_control

def get_labeled_entry(labelName, defaultText):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        label = Gtk.Label(labelName)
        hbox.pack_start(label, False, False, 10)

        entry = Gtk.Entry()
        entry.set_text(defaultText)
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

        self.entry_loc = Gtk.Entry()
        self.entry_loc.set_text("Location")
        vbox.pack_start(self.entry_loc, True, True, 0)

        button = Gtk.Button("Longitude latitude from location")
        button.connect("clicked", self.lat_lng_from_location)
        vbox.pack_start(button, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(True)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("console..")
        vbox.pack_start(self.textview, True, True, 0)

        try:
            lo, la, te = self.loader.get_values()
        except Exception as e:
            self.textbuffer.set_text(e.__str__())
            lo, la, te = 58, 10, 3400
        
        hbox, self.entry_lng = get_labeled_entry("Longitude", lo)
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_lat = get_labeled_entry("Latitude", la)
        vbox.pack_start(hbox, True, True, 0)

        hbox, self.entry_temp = get_labeled_entry("Color temperature (default 3400)", te)
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Save and refresh xflux")
        button.connect("clicked", self.save_and_update)
        vbox.pack_start(button, True, True, 0)

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
        except long_lat_getter.Rxpt as l:
            self.textbuffer.set_text(l.__str__())
            return
        self.entry_lat.set_text(str(lat))
        self.entry_lng.set_text(str(lng))

def main():
    win = EntryWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
