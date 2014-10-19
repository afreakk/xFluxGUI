class Console(object):
    def __init__(self, textview):
        self.textbuffer = textview.get_buffer()
        self.append_txt("\n\n--xfluxgui--")
    def append_txt(self, txt):
        self.textbuffer.insert_at_cursor(txt)
    def clear_txt(self):
        self.textbuffer.set_text("")
