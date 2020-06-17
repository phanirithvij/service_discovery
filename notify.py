#! /bin/python
from plyer import notification
import os


notification.notify(
    title=  '     Hello        ',
    message='     Bro          ',
    app_name='      Python script',
    timeout=4,
    #app_icon=os.path.abspath("/home/rithvij/Downloads/wifi.png")
    app_icon=os.path.abspath("/media/rithvij/Storage/Images/meme.jpg")
    #app_icon=os.path.abspath("D:/Images/meme.ico")
)
