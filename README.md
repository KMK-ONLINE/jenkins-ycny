Jenkins YCNY (Your Country Needs You)
=====================================

Ubuntu 14.04 Desktop Notification for Jenkins Build.

```
$ apt-get quickly python-gi
```


Resources
---------

* https://wiki.ubuntu.com/Quickly
* http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
* https://www.philipphoffmann.de/gnome-3-shell-extension-jenkins-ci-server-indicator/
* https://www.google.co.id/search?q=your+country+needs+you


Development
-----------

* https://wiki.gnome.org/action/show/Projects/PyGObject

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

