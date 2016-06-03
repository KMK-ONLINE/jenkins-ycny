### Jenkins YCNY (Your Country Needs You)

## Install

Ubuntu 14.04/16.04 Desktop Notification for Jenkins Build.

```
$ sudo apt-get install python-gi
```

Additional Python package:

```
$ sudo pip install -r requirements.txt
```

Test Running:

```
$ bin/jenkins-ycny -v
```

Install to Desktop and Autostart:

```
$ python setup.py
```

Resources:
* http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
* https://www.philipphoffmann.de/gnome-3-shell-extension-jenkins-ci-server-indicator/
* https://www.google.co.id/search?q=your+country+needs+you


## Development

# Quickly (Ubuntu 14.04)

Developing using Ubuntu 14.04 Quickly:

```
sudo apt-get install quickly
```

Docs:
* https://wiki.ubuntu.com/Quickly


# PyGObject (PyGI)

Version:
```
>>> import gi
>>> gi
<module 'gi' from '/usr/lib/python2.7/dist-packages/gi/__init__.pyc'>
>>> gi.__version__
'3.12.0'
>>>
```

Getting Help:
```
>>> from gi.repository import Gtk
>>> dir(Gtk)
>>> help(Gtk)
>>> dir(Gtk.Window)
>>> help(Gtk.Window)
```

For function use `__doc__` instead `help()`:
```
>>> Gtk.Window.modify_bg.__doc__
modify_bg(self, state:Gtk.StateType, color:Gdk.Color=None)
```

Docs:
* https://wiki.gnome.org/action/show/Projects/PyGObject

