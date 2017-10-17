import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import library
import module_load
import vars


class main_win:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('../ui/mainwindow.ui')
        self.builder.connect_signals(self)
        self.main_win = self.builder.get_object('opengospel_main_win')
        self.main_win_headerbar = self.builder.get_object('opengospel_main_win_headerbar')
        self.main_win_menu = self.builder.get_object('opengospel_main_win_menu')
        self.flow = Gtk.FlowBox()
        self.main_win.add(self.flow)
        for mod in module_load.loaded_modules:
            module_icon = Gtk.Image.new_from_file(vars.module_dir + '/' + mod + '/' + module_load.module_data[mod]['icon'])
            self.flow.add(module_icon)
        self.main_win.connect('destroy', lambda w: Gtk.main_quit())
        self.main_win.show_all()

class notebook:
    def __init__(self):
        self.tabs = Gtk.notebook.new()

if __name__ == "__main__":
    main_win()
    Gtk.main()
