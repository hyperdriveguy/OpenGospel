#!/usr/bin/python
import os, sys, gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit

# Working directory - change this to where OpenGospel is
wrk_dir = '/home/carson/Documents/OpenGospel'

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
    self.webview.open('file:' + wrk_dir + '/scriptures.redo/main-menu.html')
    self.webview.connect('title-changed', self.change_title)
    self.webview.connect('load-committed', self.change_current_url)
    self.webview.show()	
   

  def on_home_clicked(self, widget):
    self.webview.open('file:' + wrk_dir + '/scriptures.redo/main-menu.html')

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
 
def bookmark_it():
	Bookmarks()

def main ():
  mainApp = MainWindow()
  Gtk.main()

if __name__ == "__main__":
  main()

