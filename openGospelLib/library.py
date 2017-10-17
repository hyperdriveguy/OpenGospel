import vars
import module_load
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class library:
    def __init__(self, flowbox, mod):
        module_icon = Gtk.Image.new_from_file(vars.module_dir + '/' + mod + '/' + module_load.module_data[mod]['icon'])
        flowbox.add(module_icon)
