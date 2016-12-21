import SocketServer

import nuke
from nukescripts import utils
import nuke_listener

try:
	listener = nuke_listener.NukeListener()
	listener.start()

	def killListener():
		listener.stop()

	nuke.addOnScriptClose( killListener )
except SocketServer.socket.error as e:
	print e
	print "Using existing HTTP listener"