#!/usr/bin/python
import os, sys, gi, subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit

# Working directory - change this to where OpenGospel is
wrk_dir = '/home/carson/Documents/OpenGospel'
css_dir = wrk_dir + '/scriptures.redo/'
config = "opengospel.conf"

# Apply configuration
with open(config, "r") as getconf:
	if getconf.read(1) == "T":
		gladefile = "scriptures-csd.glade"
	elif getconf.read(1) == "F":
		gladefile = "scriptures.glade"
	else:
		gladefile = "scriptures.glade"

# OpenGospel version
ver = "0.3-dev"

class MainWindow:
	def __init__(self):
		self.builder = Gtk.Builder()
		# Get UI
		self.builder.add_from_file(gladefile)
		self.builder.connect_signals(self)
		# ToolBar
		self.navbar = self.builder.get_object("navbar")
		self.last = self.builder.get_object("last")
		self.next = self.builder.get_object("next")
		self.menu = self.builder.get_object("menu")
		self.previous = self.builder.get_object("previous")
		# About
		self.about = self.builder.get_object("about")
		# Scriptures
		self.scriptures = self.builder.get_object("scriptures")
		self.scriptures.connect('destroy', lambda w: Gtk.main_quit())
		self.scrolledwindow = self.builder.get_object("scrolledwindow")
		self.scriptures.show_all()
		# Webkit
		self.webview = WebKit.WebView()
		self.scrolledwindow.add(self.webview)
		self.webview.open('file://' + wrk_dir + '/scriptures.redo/main-menu.html')
		self.webview.connect('title-changed', self.change_title)
		self.webview.connect('load-committed', self.change_current_url)
		self.webview.show()

	def on_menu_clicked(self, widget):
		# Statically set Main Menu
		self.webview.open('file:' + wrk_dir + '/scriptures.redo/main-menu.html')

	def on_last_clicked(self, widget):
		# Go to the Previous Page
		self.webview.go_back()

	def on_next_clicked(self, widget):
		calculate_chapter()
		next_chapter = chapter + 1
		global next_url
		next_url = current_url.replace(str(chapter)+".html",str(next_chapter)+".html")
		self.webview.open(next_url)
		
	def on_previous_clicked(self, widget):
		calculate_chapter()
		prev_chapter = chapter - 1
		global prev_url
		prev_url = current_url.replace(str(chapter)+".html",str(prev_chapter)+".html")
		self.webview.open(prev_url)

	def on_aboutbutton_clicked(self, widget):
		self.about.set_version("Version " + ver)
		self.about.show()

	def on_about_response(self, widget, null):
		self.about.hide()

	# Settings
	def on_settingsbutton_clicked(self, widget):
		self.builder = Gtk.Builder()
		# Get UI
		self.builder.add_from_file("scriptures.glade")
		self.builder.connect_signals(self)
		self.settings = self.builder.get_object("settings")
		self.applysettings = self.builder.get_object("applysettings")
		self.canelsettings = self.builder.get_object("cancelsettings")
		self.csdswitch = self.builder.get_object("csdswitch")
		self.nightmodeswitch = self.builder.get_object("nightmodeswitch")
		self.restartdialog = self.builder.get_object("restartdialog")
		self.restartok = self.builder.get_object("restartok")
		self.settings.show()
		self.csdswitch.connect("notify::active", self.on_csdswitch_activate)
		self.nightmodeswitch.connect("notify::active", self.on_nightmodeswitch_activate)
		global csd_on
		global setconf
		if os.path.isfile(config) == True:
			setconf = open(config, "r+")
			csd_on = setconf.read(1)
			if csd_on == "T":
				self.csdswitch.set_active(True)
			else:
				self.csdswitch.set_active(False)
				csd_on = "F"
			nightmode_on = setconf.read(2)
			if nightmode_on == "T":
				self.nightmodeswitch.set_active(True)
			else:
				self.nightmodeswitch.set_active(False)
				nightmode_on = "F"
		else:
			setconf = open(config, "w+")
			csd_on = "F"
			nightmode_on = "F"
			self.csdswitch.set_active(False)
			self.nightmodeswitch.set_active(False)

	def on_csdswitch_activate(self, widget, gparam):
		global csd_on
		if self.csdswitch.get_active():
			csd_on = "T"
		else:
			csd_on = "F"
		
	def on_nightmodeswitch_activate(self, widget, gparam):
		global nightmode_on
		if self.nightmodeswitch.get_active():
			nightmode_on = "T"
		else:
			nightmode_on = "F"

	def on_applysettings_clicked(self, widget):
		self.restartdialog.show()
		setconf.seek(0)
		setconf.write(csd_on + nightmode_on)
		if nightmode_on == "T":
			modecss("night")
		else:
			modecss("normal")
		# For debugging the config
		# print("Wrote: " + csd_on + nightmode_on, file=sys.stderr)
		setconf.close()
	def on_cancelsettings_clicked(self, widget):
		setconf.close()
		self.settings.destroy()
	def on_restartdialog_response(self, widget, null):
		self.restartdialog.destroy()
	def on_restartok_clicked(self, widget):
		self.restartdialog.destroy()
		Gtk.main_quit()
	# Webview specific stuff
	def change_title(self, widget, frame, title):
		self.scriptures.set_title(title + " - OpenGospel " + ver)

	def change_current_url(self, widget, frame):
		global current_url
		current_url = frame.get_uri()
		self.last.set_sensitive(self.webview.can_go_back())
		
		if "menu" in current_url or "http" in current_url:
			self.next.set_sensitive(False)
			self.previous.set_sensitive(False)

		else:
			self.next.set_sensitive(True)
			self.previous.set_sensitive(True)
			if current_url == 'file://' + wrk_dir + '/scriptures.redo/bom/1nephi/1.html':
				self.previous.set_sensitive(False)

def calculate_chapter():
	global chapter
	chapter = current_url[current_url.index('file://' + wrk_dir):current_url.index('.html')]
	isInt = False
	while isInt == False:
		try:
			chapter = int(chapter)
			isInt = True
		except ValueError:
			chapter = chapter[1:]

def modecss(style):
	subprocess.run(["rm", css_dir + "menu.css", css_dir + "scriptures.css"], check=True)
	subprocess.run(["cp", "-T", css_dir + "themes/" + style + "menu.css", css_dir + "menu.css"], check=True)
	subprocess.run(["cp", "-T", css_dir + "themes/" + style + "scriptures.css", css_dir + "scriptures.css"], check=True)

if __name__ == "__main__":
	MainWindow()
	Gtk.main()
