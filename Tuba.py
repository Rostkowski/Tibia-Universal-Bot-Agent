from tkinter import *
from win32gui import GetWindowText, GetForegroundWindow
import PIL.ImageGrab
import time
import autoit
import keyboard
import threading
import configparser
import pathlib


def spell_thread():
    threadSpell = threading.Thread(target=spell, name="Spell Thread")
    threadSpell.start()



root = Tk()
root.title("TUBA v.0.0.1")
root.configure(bg="#18110f")

hotkey = ""
HPCoords = (0, 0)
HPCoords_x = 0
HPCoords_y = 0
hpBarColor_r = 0
hpBarColor_g = 0
hpBarColor_b = 0
hpBarColor = (0, 0, 0)
clientName = ""


def getpix(i_x, i_y):
	return PIL.ImageGrab.grab().load()[i_x, i_y]

def getCoordsAndPixelColor():
    global HPCoords_x
    global HPCoords_y
    global hpBarColor
    global pixelColorSelectedLabel
    global coordsSelectedLabel
    global hpBarColor_r
    global hpBarColor_g
    global hpBarColor_b
    while True:
        if keyboard.is_pressed('esc'):
            HPCoords = autoit.mouse_get_pos()
            HPCoords_x = HPCoords[0]
            HPCoords_y = HPCoords[1]
            hpBarColor = getpix(HPCoords_x, HPCoords_y)
            hpBarColor_r = hpBarColor[0]
            hpBarColor_g = hpBarColor[1]
            hpBarColor_b = hpBarColor[2]
            pixelColorSelectedLabel = Label(text=str(hpBarColor_r)+", "+str(hpBarColor_g)+", "+str(hpBarColor_b), fg="white", bg="#18110f")
            pixelColorSelectedLabel.grid(row=2, column=1)
            coordsSelectedLabel = Label(text=str(HPCoords_x)+", "+str(HPCoords_y), fg="white", bg="#18110f") 
            coordsSelectedLabel.grid(row=3, column=1)
            return

def loadSettings():
    global hotkey
    global HPCoords_x
    global HPCoords_y
    global hpBarColor
    global clientName
    global hotkeySelection
    global clientSelection
    global pixelColorSelectedLabel
    global coordsSelectedLabel
    global hpBarColor_r
    global hpBarColor_g
    global hpBarColor_b

    config = configparser.ConfigParser()
    config.read('settings.ini')
    settings = config['DEFAULT']
    hotkey = str(settings['hotkeyselection'])
    HPCoords_x = settings['hpcoords_x']
    HPCoords_y = settings['hpcoords_y']
    hpBarColor_r = settings['hpbarcolor_r']
    hpBarColor_g = settings['hpbarcolor_g']
    hpBarColor_b = settings['hpbarcolor_b']
    clientName = str(settings['clientname'])


    hotkeySelection = Entry(root, width=5, fg="white", bg="#18110f")
    clientSelection = Entry(root, width=10, fg="white", bg="#18110f")
    pixelColorSelectedLabel = Label(text=str(hpBarColor_r)+", "+str(hpBarColor_g)+", "+str(hpBarColor_b), fg="white", bg="#18110f")
    coordsSelectedLabel = Label(text=str(HPCoords_x)+", "+str(HPCoords_y), fg="white", bg="#18110f") 

    hotkeySelection.insert(0, hotkey)
    clientSelection.insert(0, clientName)
    coordsSelectedLabel.grid(row=3, column=1)
    clientSelection.grid(row=1, column=1)
    pixelColorSelectedLabel.grid(row=2, column=1)
    hotkeySelection.grid(row=0, column=1)


def spell():
    settingsSaver()
    print(HPCoords_x)
    print(HPCoords_y)
    while True:
        if var.get() == 1:
            if GetWindowText(GetForegroundWindow()) == clientSelection.get():
                if getpix(int(HPCoords_x), int(HPCoords_y)) != (int(hpBarColor_r), int(hpBarColor_g), int(hpBarColor_b)):
                    time.sleep(0.25)
                    autoit.send("{" + hotkeySelection.get() + "}")
        elif var.get() == 0:
            print("konczymy")
            return


var = IntVar()

hotkeyLabel = Label(text="Spell Hotkey: ", fg="white", bg="#18110f")
hotkeyLabel.grid(row=0, column=0)

hotkeySelection = Entry(root, width=5, fg="white", bg="#18110f")
hotkeySelection.insert(0, hotkey)
hotkeySelection.grid(row=0, column=1)

spellUsageCheckBox = Checkbutton(root, text="Use Spell", variable=var, fg="yellow", bg="#18110f")
spellUsageCheckBox.deselect()
spellUsageCheckBox.grid(row=0, column=2)

clientLabel = Label(text="Client window name: ", fg="white", bg="#18110f")
clientLabel.grid(row=1, column=0)

clientSelection = Entry(root, width=10, fg="white", bg="#18110f")
clientSelection.insert(0, clientName)
clientSelection.grid(row=1, column=1)

pixelColorSelectionLabel = Label(text="Pixel color of HP bar: ", fg="white", bg="#18110f")
pixelColorSelectionLabel.grid(row=2, column=0)

pixelColorSelectedLabel = Label(text=str(hpBarColor_r)+", "+str(hpBarColor_g)+", "+str(hpBarColor_b), fg="white", bg="#18110f")
pixelColorSelectedLabel.grid(row=2, column=1)

xyCoordsLabel = Label(text="Coordinates of HP section you'd like to heal from: ", fg="white", bg="#18110f")
xyCoordsLabel.grid(row=3, column=0)

coordsSelectedLabel = Label(text=str(HPCoords_x)+", "+str(HPCoords_y), fg="white", bg="#18110f")
coordsSelectedLabel.grid(row=3, column=1)

coordsGetLabel = Label(text="Press button, move your mouse to the HP area and press ESC >>", fg="white", bg="#18110f")
coordsGetLabel.grid(row=4, column=0)

coordsGet = Button(root, text="Get HP pos", command=getCoordsAndPixelColor, width=10, fg="white", bg="#18110f")
coordsGet.grid(row=4, column=1)

saveSettings = Button(root, text="Save and Run", command=spell_thread, width=10, fg="white", bg="#18110f")
saveSettings.grid(row=5, column=1)

loadSettings = Button(root, text="Load settings", command=loadSettings, width=10, fg="white", bg="#18110f")
loadSettings.grid(row=5, column=2)

def settingsSaver():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'hotkeySelection': str(hotkeySelection.get()),
                        'HPCoords_x': HPCoords_x,
                        'HPCoords_y': HPCoords_y,
                        'hpBarColor_r': hpBarColor_r,
                        'hpBarColor_g': hpBarColor_g,
                        'hpBarColor_b': hpBarColor_b,
                        'clientName': str(clientSelection.get())}
    with open(pathlib.Path.home() / 'settings.ini', 'w') as configfile:
        config.write(configfile)
root.mainloop()