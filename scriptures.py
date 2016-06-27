#!/usr/bin/python
import os, sys, gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit

# Working directory - change this to where OpenGospel is
wrk_dir = '/home/carson/Programming/OpenGospel'

# OpenGospel version
ver = "v0.1-dev"

class MainWindow:
  def __init__(self):
    self.builder = Gtk.Builder()
   
    self.builder.add_from_file("scriptures.glade")
    self.builder.connect_signals(self)

    self.toolbar1 = self.builder.get_object("navbar")
    self.back = self.builder.get_object("back")
    self.forward = self.builder.get_object("forward")
    self.refresh = self.builder.get_object("home")
    self.bookmark_button = self.builder.get_object("bookmark")
    self.window = self.builder.get_object("scriptures")
    self.window.connect('destroy', lambda w: Gtk.main_quit())
    self.scrolledwindow = self.builder.get_object("scrolledwindow")
    self.window.show_all()

    self.webview = WebKit.WebView()
    self.scrolledwindow.add(self.webview)
    self.webview.open('file:' + wrk_dir + '/scriptures.nephi.org/docbook/index.html')
    self.webview.connect('title-changed', self.change_title)
    self.webview.connect('load-committed', self.change_current_url)
    self.webview.show()	
   

  def on_home_clicked(self, widget):
    self.webview.open('file:' + wrk_dir + '/scriptures.nephi.org/docbook/index.html')

  def on_back_clicked(self, widget):
    self.webview.go_back()
    
  def on_forward_clicked(self, widget):
     self.webview.go_forward()
     
  def on_bookmark_clicked(self, widget):
     bookmark_it()

  def change_title(self, widget, frame, title):
	self.window.set_title(title + " - OpenGospel " + ver)
     
  def change_current_url(self, widget, frame):
     current_url = frame.get_uri()
     self.back.set_sensitive(self.webview.can_go_back() )
     self.forward.set_sensitive(self.webview.can_go_forward() )
 
class Bookmarks:
	def _init_(self):
		self.builder = Gtk.Builder()
   
		self.builder.add_from_file("bookmarks.glade")
		self.builder.connect_signals(self)

		self.box1 = self.builder.get_object("box1")
		self.box2 = self.builder.get_object("box2")
		self.delete_button = self.builder.get_object("delete")
		self.add_button = self.builder.get_object("add")
		self.load_button = self.builder.get_object("load")
		self.bookmark_choose = self.builder.get_object("bookmark_choose")
		self.bookmark_window = self.builder.get_object("bookmarks")
		self.bookmark_list = self.builder.get_object("bookmark_list")
		self.bookmark_window.show_all()
		
		if self.window.connect('destroy'):
			self.bookmark_window.hide_all()
 
	def load_bookmarks():
		print("Need help implementing this")
  
def bookmark_it():
	Bookmarks()

def main ():
  mainApp = MainWindow()
  Gtk.main()

if __name__ == "__main__":
  main()

