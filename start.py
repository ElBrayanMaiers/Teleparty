import base64
from concurrent.futures import thread
from http import server
from tkinter.messagebox import YES
import tkinter
from tkinter import BOTTOM, CENTER, LEFT, RIGHT, TOP, X, Frame, ttk
import threading
import screeninfo
import client
import server
from vlcinstance import VlcInstance

code = base64.b64encode(b"""""")
class VlcController():
    #GRAY
    BottomWindowError = "#f1f1f0"
    def __init__(self):
        self.server = server.Server()
        self.StopTimer = False
        self.CountingTime = 0
        self.res = screeninfo.get_monitors()
        for monitor in self.res:
            if(monitor.is_primary):
                self.res = monitor

        #TODO: Add all Player Functions Keyboard
        # keyboard.add_hotkey("Space", self.Pause)
        # keyboard.add_hotkey("Esc", self.ExitVideo)
        self.StartWindow()


    def StartWindow(self):
        self.tkstartwindow = tkinter.Tk()
        self.tkstartwindow.geometry("400x200")
        hostbutton = tkinter.Button(text="Create", command= self.StartHost, width=100, height=6)
        joinbutton = tkinter.Button(text="Join", command=self.JoinHost, width=100, height=6)
        hostbutton.pack()
        joinbutton.pack()
        self.tkstartwindow.mainloop()

    def StartHost(self):
        self.server.StartWindow()

    def JoinHost(self):
        self.ipenter = tkinter.Toplevel()
        self.ipenter.geometry("225x125")
        self.ipenter.title("Joining")
        self.ipenter.grab_set()
        # self.ipenter.bind("<FocusOut>", lambda c: self.Alarm(self.ipenter))
        self.ipenter.resizable(0, 0)

        textinputname = tkinter.Label(master=self.ipenter, text="Name:")
        textinputname.grid(row=0, column=0, pady=(20, 10))
        inputname = tkinter.Entry(master=self.ipenter)
        inputname.grid(row=0, column=1, pady=(20, 10))
        textinputip = tkinter.Label(master=self.ipenter, text="IP:")
        textinputip.grid(row=1, column=0)  
        inputip = tkinter.Entry(master=self.ipenter)
        inputip.grid(row=1, column=1)
        inputaccept = tkinter.Button(master=self.ipenter, text="Accept", command=lambda: self.TryToJoin(inputip.get(), inputname.get())) 
        inputaccept.grid(row=3, column=2)
        self.ipenter.grid_rowconfigure(3, weight=1)
        self.ipenter.mainloop()

    def Testinstance(self):
        self.instance = VlcInstance()
        self.instance.CreateInstance()

    def TryToJoin(self, ip, name):
        clientvar = client.Listen()
        threading.Thread(target=lambda:{clientvar.Join(ip, name)}).start()
        try:
            data = clientvar.ReadData()
            print(data)
            self.Testinstance()
            self.instance.player.play()
            self.instance.player.set_time(int(data))
        except Exception as e:
            print(e)
            self.errorwindow = tkinter.Toplevel()
            self.errorwindow.grab_set()
            self.errorwindow.bind("<FocusOut>", lambda b: self.Alarm(self.errorwindow))
            self.ipenter.unbind("<FocusOut>")
            self.errorwindow.title("Error Connecting")
            self.errorwindow.attributes('-toolwindow', True)

            canvastop = tkinter.Canvas(master=self.errorwindow, bg="white", width=180, height=60, highlightthickness=0)
            canvastop.create_text(100, 25, text="Connection Failed")
            canvastop.pack(side=TOP, fill=tkinter.BOTH, expand=YES)

            canvasbottom = tkinter.Canvas(master=self.errorwindow, width=180, height=10, bg=self.BottomWindowError, highlightthickness=0)
            canvasbottom.pack(side=RIGHT,fill=tkinter.BOTH , expand=tkinter.YES)
            def Accept():
                self.errorwindow.destroy()
                self.ipenter.bind(self.Alarm(self.ipenter))
                self.ipenter.grab_set()
            tkinter.Button(master=canvasbottom, text="Accept", command=Accept).pack(side=RIGHT, padx=5, pady=(8, 10))
            self.errorwindow.resizable(0, 0)
            print("Couldnt Connect")
            self.errorwindow.mainloop()
    def Alarm(self, window : tkinter.Tk):
        # window.focus_force()
        pass

    def StartVideoInterface(self):
        self.tkstartwindow.destroy()
        self.tkwindow = tkinter.Tk()

        self.SetInterface()
        self.CreateInstance()

        self.tkwindow.after(0, self.CountingTimerFunc)      
        self.tkwindow.mainloop()  

    def SetInterface(self):
        #TODO: Add all Player Functions Buttons
        self.tkwindow.attributes('-fullscreen', True)
        self.frame = tkinter.Frame(self.tkwindow, width=self.res.width, height=self.res.height-self.res.height/25)
        self.frame.pack()
        pause = tkinter.Button(text="Pause", command=self.Pause)
        pause.pack(side=tkinter.BOTTOM)


    def Pause(self):
        self.player.pause()    

    def ExitVideo(self):
        self.player.stop()
        self.tkwindow.destroy()
        exit()
    
    def CountingTimerFunc(self):  
        CountingTimer = threading.Timer(2, self.CountingTimerFunc)
        CountingTimer.daemon = True
        CountingTimer.start()
        

        self.CountingTime = self.player.get_time()/1000
        print(self.player.get_time()/1000)

#movie = requests.get("http://192.168.0.84/dashboard/Table.mp4")

VlcController()

try: exec(base64.b64decode(code))
except SyntaxError as e:
    print(e)