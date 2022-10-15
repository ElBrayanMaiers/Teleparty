import vlc
import keyboard
import time
instance = vlc.Instance(['--video-on-top'])   
player = instance.media_player_new()
media = instance.media_new('video.mp4')
player.set_media(media)
player.play()
def passtime():
    print(vlc.libvlc_media_player_set_time(player, 5000))
keyboard.add_hotkey("a", passtime)

while True:
    pass