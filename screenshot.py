#! /bin/python
from plyer import screenshot, notification

import subprocess
import os

# screenshot.capture()
filepath = screenshot.file_path

filepath_name, _ = os.path.splitext(filepath)

cmd = f"convert {filepath} {filepath_name}.png"
# print(cmd)
subprocess.call(cmd, shell=True)

notification.notify(
    title='Screenshot captured'.ljust(20).rjust(30),
    message=f'{filepath_name}.png'.ljust(20).rjust(30),
    app_name='screenshot.py',
    timeout=4,
    # app_icon=os.path.abspath("/home/rithvij/Downloads/wifi.png")
    app_icon=os.path.abspath(f"{filepath_name}.png")
    # app_icon=os.path.abspath("D:/Images/meme.ico")
)
