import threading
from time import sleep
import tkinter
from tkinter import CENTER, Grid, filedialog
from turtle import right
from winreg import REG_DWORD_LITTLE_ENDIAN
import vlc
import base64
import keyboard
# code = base64.b64encode(b""" 
#    """)

# exec(base64.b64decode(code))

class VlcInstance():
    def __init__(self):
        self.x = 0
        self.fullscreenStatus = 0
        self.CreateInstance()

    def CreateInstance(self):        
        self.instance = vlc.Instance(['--video-on-top'])   
        self.player = self.instance.media_player_new()
        media = self.instance.media_new('video.mp4')
        self.player.set_media(media)
        threading.Thread(target=self.CreateInterface).start()
        sleep(1)
        # threading.Thread(target=self.ControlTimeLine).start()
        keyboard.add_hotkey("l", self.ButtonsHide)
        keyboard.add_hotkey("f11", self.ManageFullscreen)
        keyboard.add_hotkey("space", self.player.pause)
        keyboard.add_hotkey("right arrow", lambda: self.player.set_time(self.player.get_time()+ 5000))
        keyboard.add_hotkey("left arrow", lambda: self.player.set_time(self.player.get_time()- 5000))
        self.ControlTimeLine()

    def ControlTimeLine(self):
        self.length = self.player.get_length()
        while True:
            self.timebar.set(1000/self.length*self.player.get_time())
            sleep(1)
            pass

    def ManageFullscreen(self):
        if self.fullscreenStatus == 0:
            self.root.attributes("-fullscreen", True)
            self.fullscreenStatus = 1
        else:
            self.root.attributes("-fullscreen", False)
            self.fullscreenStatus = 0

    def ButtonsHide(self):
        if self.x == 0:
            self.x = 1
            self.controlframe.grid_remove()
            self.display.grid_remove()
            self.display.place(relheight=1, relwidth=1)
        else:
            self.x = 0
            self.controlframe.grid()
            self.display.place_forget()
            self.display.grid()

    def on_closing(self):
        self.root.destroy()
        self.root.quit()

    def CreateInterface(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.display = tkinter.Frame(master=self.root, width=1600, height=900)
        self.display.rowconfigure(2 , weight=1)
        self.display.columnconfigure(2, weight=1)
        self.display.grid(column=0, row=0, sticky="news")

        self.controlframe = tkinter.Frame(master=self.root)
        self.controlframe.rowconfigure(0, weight=1)
        self.controlframe.columnconfigure(0, weight=1)
        self.controlframe.grid(column=0, row=1, sticky="wse")

        buttonframes = tkinter.Frame(master=self.controlframe, bg="red")
        buttonframes.grid(column=0, row=1)

        inputmovie = tkinter.Button(master=self.controlframe, text="Select Movie", command=self.InputMovie).grid(column=0, row=1, sticky="w")
        leftbutton = tkinter.Button(master=buttonframes, text="<", command=lambda: self.player.set_time(self.player.get_time()- 5000)).grid(column=1, row=1)
        pausebutton = tkinter.Button(master=buttonframes, text="ll", command=self.player.pause).grid(column=2, row=1)
        rightbutton = tkinter.Button(master=buttonframes, text=">", command=lambda: self.player.set_time(self.player.get_time()+ 5000)).grid(column=3, row=1)

        self.timebar = tkinter.Scale(master=self.controlframe, from_=0, to=1000, orient=tkinter.HORIZONTAL, length=1000)
        self.timebar.grid(column=0, row=0)
        # self.timebar.bind("<Button-1>", )
        keyboard.add_hotkey("d", threading.Thread(target=self.SkipTimeBar).start)

        self.volumecontrol = tkinter.Scale(master=self.controlframe, from_=100, to=0, orient=tkinter.VERTICAL, command=self.SetVolume, length=50, sliderlength=15)
        self.volumecontrol.set(0)
        self.volumecontrol.bind("<Button-1>", self.SkipVolumeControl)
        self.volumecontrol.grid(column=2, row=1)
        self.player.set_xwindow(self.display.winfo_id())
        self.player.set_hwnd(self.display.winfo_id())
        self.player.play()
        self.root.mainloop()

    def SkipTimeBar(self):
        # self.timebar.set(event.x)
        self.player.set_time(5000)
        # self.player.set_time(int(self.length/1000*event.x))

    def SkipVolumeControl(self, event):
        self.volumecontrol.set(100 - event.y*2)

    def SetVolume(self, volume):
        self.player.audio_set_volume(int(volume))

    def InputMovie(self):
        dialog = filedialog.askopenfile(initialdir="/", title="Select Movie", filetypes=(("Mp4", "*.mp4"), ("Avi", "*.avi")))
        media = self.instance.media_new(dialog.name)
        self.player.set_media(media)
        self.player.play()