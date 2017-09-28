#!/usr/bin/python
'''
Copyright (C) 2017

This file is part of OpenGospel.

OpenGospel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenGospel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenGospel.  If not, see <http://www.gnu.org/licenses/>.
'''
import os, gi, subprocess

# Only used in debugging
if __debug__:
	import sys

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2 as WebKit

# OpenGospel Constants
# Working directory - change this to where OpenGospel is
bin_dir = '/home/carson/Documents/coding/opengospel'
share_dir = bin_dir
css_dir = share_dir + '/scriptures.redo'
config_dir = bin_dir
config = config_dir + '/opengospel.conf'
# OpenGospel version
ver = "0.3"

class ConfigInit:
	def modecss(style):
		try:
			subprocess.run(["rm", css_dir + "/menu.css", css_dir + "/scriptures.css"], check=True)
		except FileNotFoundError:
			pass
		subprocess.run(["cp", "-T", share_dir + "/scriptures.redo/themes/" + style + "menu.css", css_dir + "/menu.css"], check=True)
		subprocess.run(["cp", "-T", share_dir + "/scriptures.redo/themes/" + style + "scriptures.css", css_dir + "/scriptures.css"], check=True)

	def glade_init(conf_file):
		# Globally declare the glade file
		global gladefile
		try:
			with open(conf_file, "r") as getconf:
				if getconf.read(1) == "T":
					gladefile = share_dir + "/scriptures-csd.glade"
				elif getconf.read(1) == "F":
					gladefile = share_dir + "/scriptures.glade"
				else:
					gladefile = share_dir + "/scriptures.glade"
		except FileNotFoundError:
			# First Run
			gladefile = share_dir + "/scriptures.glade"
			try:
				subprocess.run(["mkdir", "-pv", config_dir], check=True)
			except FileNotFoundError:
				pass
			# If no config is found, it is likely that no CSS is there either
			subprocess.run(["cp", "-T", share_dir + "/scriptures.redo/themes/" + "normalmenu.css", css_dir + "/menu.css"], check=True)
		subprocess.run(["cp", "-T", share_dir + "/scriptures.redo/themes/" + "normalscriptures.css", css_dir + "/scriptures.css"], check=True)

		if __debug__:
			print("UI file: " + gladefile)


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
		# Scriptures
		self.scriptures = self.builder.get_object("scriptures")
		self.scriptures.connect('destroy', lambda w: Gtk.main_quit())
		self.scrolledwindow = self.builder.get_object("scrolledwindow")
		self.loadbar = self.builder.get_object("loadbar")
		self.scriptures.show_all()
		self.loadbar.hide()
		# Webkit
		#self.usercontentmanager = WebKit.UserContentManager.new()
		#self.stylesheet = WebKit.UserStyleSheet.new("/home/carson/Documents/coding/opengospel/scriptures.redo/themes/nightmenu.css", WebKit.UserContentInjectedFrames(0), WebKit.UserStyleLevel(0))
		#self.usercontentmanager.add_style_sheet(self.stylesheet)
		#self.webview = WebKit.WebView.new_with_user_content_manager(self.usercontentmanager)
		self.webview =WebKit.WebView.new()
		self.scrolledwindow.add(self.webview)
		self.webview.load_uri('file://' + share_dir + '/scriptures.redo/main-menu.html')
		self.webview.connect('notify::title', self.change_title)
		self.webview.connect('load-changed', self.change_current_url)
		self.webview.show()

	def on_menu_clicked(self, widget):
		# Statically set Main Menu
		self.webview.load_uri('file:' + share_dir + '/scriptures.redo/main-menu.html')

	def on_last_clicked(self, widget):
		# Go to the Previous Page
		self.webview.go_back()

	def on_next_clicked(self, widget):
		calculate_chapter()
		next_chapter = chapter + 1
		global next_url
		next_url = current_url.replace(str(chapter)+".html",str(next_chapter)+".html")
		self.webview.load_uri(next_url)

	def on_previous_clicked(self, widget):
		calculate_chapter()
		prev_chapter = chapter - 1
		global prev_url
		prev_url = current_url.replace(str(chapter)+".html",str(prev_chapter)+".html")
		self.webview.load_uri(prev_url)

	def on_aboutbutton_clicked(self, widget):
		# About
		self.builder.add_from_file(gladefile)
		self.builder.connect_signals(self)
		self.about = self.builder.get_object("about")
		self.about.set_version("Version " + ver)
		self.about.show_all()

	def on_about_close(self, widget, null):
		self.about.hide()

	# Settings
	def on_settingsbutton_clicked(self, widget):
		self.builder = Gtk.Builder()
		# Get UI
		self.builder.add_from_file(gladefile)
		self.builder.connect_signals(self)
		self.settings = self.builder.get_object("settings")
		self.applysettings = self.builder.get_object("applysettings")
		self.cancelsettings = self.builder.get_object("cancelsettings")
		self.csdswitch = self.builder.get_object("csdswitch")
		self.nightmodeswitch = self.builder.get_object("nightmodeswitch")
		self.restartdialog = self.builder.get_object("restartdialog")
		self.restartok = self.builder.get_object("restartok")
		self.settings.show_all()
		self.restartdialog.hide()
		self.csdswitch.connect("notify::active", self.on_csdswitch_activate)
		self.nightmodeswitch.connect("notify::active", self.on_nightmodeswitch_activate)
		global nightmode_on
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
			if __debug__:
				print("csd_on: " + csd_on, file=sys.stderr)

			nightmode_on = setconf.read(2)
			if nightmode_on == "T":
				self.nightmodeswitch.set_active(True)
			else:
				self.nightmodeswitch.set_active(False)
				nightmode_on = "F"
			if __debug__:
				print("nightmode_on: " + nightmode_on, file=sys.stderr)
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
			ConfigInit.modecss("night")
		else:
			ConfigInit.modecss("normal")
		self.applysettings.set_sensitive(False)
		self.cancelsettings.set_sensitive(False)
		# For debugging the config
		if __debug__:
			print("Wrote: " + csd_on + nightmode_on, file=sys.stderr)
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
	def change_title(self, widget, title):
		title_str = str(self.webview.get_title())
		self.scriptures.set_title(title_str + " - OpenGospel " + ver)

	def change_current_url(self, widget, frame):
		global current_url
		current_url = self.webview.get_uri()
		self.last.set_sensitive(self.webview.can_go_back())

		if "http" in current_url:
			if self.webview.get_estimated_load_progress() != 1:
				self.loadbar.show()
				self.loadbar.set_fraction(self.webview.get_estimated_load_progress())
				print(self.webview.get_estimated_load_progress(), file=sys.stderr)
			else:
				self.loadbar.hide()
			
			
			
		if "menu" in current_url or "http" in current_url:
			self.next.set_sensitive(False)
			self.previous.set_sensitive(False)

		else:
			self.next.set_sensitive(True)
			self.previous.set_sensitive(True)
			if current_url == 'file://' + share_dir + '/scriptures.redo/bom/1nephi/1.html':
				self.previous.set_sensitive(False)

def calculate_chapter():
	global chapter
	chapter = current_url[current_url.index('file://' + share_dir + '/scriptures.redo/'):current_url.index('.html')]
	isInt = False
	while isInt == False:
		try:
			chapter = int(chapter)
			isInt = True
		except ValueError:
			chapter = chapter[1:]

if __name__ == "__main__":
	ConfigInit.glade_init(config)
	MainWindow()
	Gtk.main()
