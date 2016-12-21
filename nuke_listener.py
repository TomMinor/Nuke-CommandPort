import SocketServer
import BaseHTTPServer
import threading
import time
import ntpath
import sys
import os

import nuke
from nukescripts import utils

# try:
#     stopListener()
# except NameError:
#     pass

class TCPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        post_data_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(post_data_len)

        print post_data
        sys.stdout.flush()

        updatedNodes = 0
        for blinknode in nuke.allNodes("BlinkScript"):
            print blinknode
            if os.path.samefile(post_data, blinknode.knob("kernelSourceFile").getValue()):
                print "Found {0}, reloading".format(blinknode.name())

                # Force control panel to be shown or else the knobs won't execute properly 
                nuke.executeInMainThread(blinknode.showControlPanel, ())
                # nuke.executeInMainThread(blinknode.knob("clearKernelSource").execute, ())
                nuke.executeInMainThread(blinknode.knob("reloadKernelSourceFile").execute, ())
                # nuke.executeInMainThread(blinknode.hideControlPanel, ())

                updatedNodes += 1

        nuke.debug( "Updated {0} Blink nodes in script {1}".format(updatedNodes,post_data) )
       
        self.send_response(200) # OK Response

        return

    def do_GET(self):
        return

class NukeListener:
    def __init__(self, port=8000):
        self.port = port
        self.commandListener = SocketServer.TCPServer(("localhost", port), TCPHandler)

    def __backgroundListener(self):
        self.commandListener.serve_forever()

    def start(self):
        self.listenerThread = threading.Thread(target=self.__backgroundListener)
        self.listenerThread.start()
    
    def stop(self):
        self.commandListener.shutdown()
        self.commandListener.socket.close()
        self.commandListener.server_close()
        self.listenerThread.join()


if __name__ == "__main__":
    import atexit

    listener = nuke_listener.NukeListener()
    listener.start()

    def killListener():
        listener.stop()

    atexit.register(killListener)