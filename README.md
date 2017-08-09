# Nuke Command Port

A simple HTTP server interface running within Nuke that listens for commands from external apps, such as sending Python commands from an external text editor.

## Installation

Simply use ```nuke.pluginAddPath``` to register the plugin in the ```.nuke/init.py``` in your home directory, like so:
```
import nuke
nuke.pluginAddPath('/home/tom/src/Nuke-CommandPort')
```
