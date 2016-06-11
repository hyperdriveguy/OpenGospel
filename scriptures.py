#!/usr/bin/python
import gtk, webkit

# OpenGospel version
ver = "v0.0.1"

# Main Window
class MainWindow():

    def __init__(self):
		
        # Create window
        self.window = gtk.Window()
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.set_default_size(1024, 768)

        # Create navigation bar
        self.navBar = gtk.HBox()

        self.back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.forward = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.home = gtk.ToolButton(gtk.STOCK_HOME)

        self.back.connect('clicked', self.go_back)
        self.forward.connect('clicked', self.go_forward)
        self.home.connect('clicked', self.home_page)

        self.navBar.pack_start(self.back, False)
        self.navBar.pack_start(self.forward, False)
        self.navBar.pack_start(self.home, False)

        # Create view for webpage
        self.view = gtk.ScrolledWindow()
        self.scriptures = webkit.WebView()
        self.scriptures.open('file:///home/carson/Programming/OpenGospel/scriptures.nephi.org/docbook/index.html')
        self.scriptures.connect('title-changed', self.change_title)
        self.view.add(self.scriptures)

        # Add everything and initialize
        self.container = gtk.VBox()
        self.container.pack_start(self.navBar, False)
        self.container.pack_start(self.view)

        self.window.add(self.container)
        self.window.show_all()
        gtk.main()

    def change_title(self, widget, frame, title):
        self.window.set_title(title + " - OpenGospel " + ver)

    def go_back(self, widget):
        self.scriptures.go_back()

    def go_forward(self, widget):
        self.scriptures.go_forward()

    def home_page(self, widget):
        self.scriptures.open('file:///home/carson/Programming/OpenGospel/scriptures.nephi.org/docbook/index.html')

mainWindow = MainWindow()
