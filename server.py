import socket
from tkinter.tix import Tree
from turtle import onclick
from urllib.request import urlopen
import tkinter
import threading
import time
import vlcinstance
import base64
shareip = str(urlopen('https://api.ipify.org?format=json').read()).replace('b\'{"ip":"', "").replace('"}\'', "")
code = base64.b64encode(b"""class Server():
    def __init__(self):
        self.stoploop = False


    def StartWindow(self):
        self.hostwindow = tkinter.Toplevel()
        publicip = tkinter.Canvas(master=self.hostwindow, width=400, height=100)
        publicip.create_text(200, 50, text=shareip)
        publicip.pack()
        startbutton = tkinter.Button(text="Start", master=self.hostwindow, command=threading.Thread(target=self.CreatePlayerInstance).start).pack()
        self.hostwindow.protocol("WM_DELETE_WINDOW", self.OnClose)
        threading.Thread(target=self.StartHost).start()
        self.hostwindow.mainloop()

    def CreatePlayerInstance(self):
        self.instance = vlcinstance.VlcInstance()
        self.instance.CreateInstance()

    def StartHost(self):
        try:
            ip, port = socket.gethostbyname(socket.gethostname()), 80
            self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host.bind((ip, port))
            self.host.listen(5)
            joinerslist = {}   
            while True:
                (clientsocket, address) = self.host.accept()
                clientsocket.sendall(str(self.instance.player.get_time()).encode("utf-8"))
                received = clientsocket.recv(1024).decode("utf-8")
                if(received.startswith("Nm")): #Check if the message received is a name with Nm
                    name = received.replace("Nm", "")
                    joinerlabel = tkinter.Label(self.hostwindow, text=received.replace("Nm", ""))
                    joinerslist[name] = joinerlabel
                    joinerlabel.pack()
                while True:
                    try:
                        data = clientsocket.recv(1024)
                    except Exception as e:
                        print("ServerTry: " + str(e))
                        for k, v in joinerslist.items():
                            v: tkinter.Label
                            v.destroy()
                        break
                    time.sleep(1)
        except Exception as e:
            print("All: " + str(e)) 
            return         

    def OnClose(self):
        self.host.close()
        self.hostwindow.destroy()""")


exec(base64.b64decode(code))