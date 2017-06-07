# OpenGospel 0.3-dev
Read your scriptures on your computer. Completely disconnected from the internet.

### What is OpenGospel?
OpenGospel is a tool to read the Standard Works (The King James Version of the Bible, The Book of Mormon, Doctrine and Covenants and Pearl of Great Price.)
It was inspired by the application "Gospel Library". Sadly, Gospel Library does not have a Linux port. That's why I started this project.
The goal of this project is to bring an open source and redistributable set of scriptures that works on Unix-like systems.

### What Operating Systems will it work on?
In theory, anything that works with Python and GTK 3. (Possibly including Windows, but that is not the goal of this project.)
Only tested on Linux (Ubuntu Mate 16.04, Kubuntu 16.04, and Arch Linux).

### How does OpenGospel work?
Offline functionality is achieved by having local HTML files, which OpenGospel reads from using Webkit.

### How do I test it?
First use:
1. Install Python 3, Webkit2GTK, and Python GObject from your distribution's repositories.
2. Download and extract OpenGospel
3. Open a terminal
4. Change to the directory you unpacked OpenGospel
5. Run chmod +x scriptures.py
6. Run by typing  ./scriptures.py
    
Every other use:
1. Open a terminal
2. Change to the directory you unpacked OpenGospel
3. Run by typing  ./scriptures.py

### How can I help?
* Take a look at Issues page and help resolve them.
* Test OpenGospel on other operating systems.
* Test for bugs.
* Create packages (.deb, .rpm, etc...)
