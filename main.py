'''

(c) Paul Florence 2016

This file is part of Mp3CoverGenerator.
Mp3CoverGenerator is free software: you can redistribute it and / or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

Mp3CoverGenerator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Mp3CoverGenerator. If not, see < http://
    www.gnu.org / licenses / >.2
'''
import os, tkinter, json, Settings, cairo, argparse, sys
from tkinter import filedialog, colorchooser
from mutagen.easyid3 import EasyID3

# --------- Argument parser --------- #

parser = argparse.ArgumentParser(description='Generate a cover from mp3 tag (and more)')
parser.add_argument('--file','-f', help="Pass a/some file(s) to process")
parser.add_argument('--directory','-d', help="Pass a directory to process", nargs='+')
parser.add_argument('--sort', '-s', help="Choose a sorting option, default: by alphabeletical order from the title field. Choose between: byTitle, byFilename, by tagNumber.")

# --------- Function declaration --------- #

#Ask the user for a color and store it in a Settings object
def pickBPMColor():
    RGBColor = tkinter.colorchooser.askcolor(Settings.cairoColorToTkColor(Settings.programSettings.textBPMColor))
    if RGBColor[0]:
        Settings.programSettings.textBPMColor = ([RGBColor[0][0]/255, RGBColor[0][1]/255, RGBColor[0][2]/255])

#Add a track to the cairo context matchin the specified user input stored in a Settings object
def displayTrack(cr, trackname, tracknumber):
    audio = EasyID3(trackname)

    cr.set_source_rgb(0.0, 0.0, 0.0)
    cr.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(Settings.programSettings.textSize)

    if 'title' in audio:
        title = audio['title'][0]
        cr.move_to(0.05,(0.01+Settings.programSettings.textVerticalOffset)*tracknumber+Settings.programSettings.textVerticalPos)
        cr.show_text(title)

    cr.set_source_rgb(Settings.programSettings.textBPMColor[0], Settings.programSettings.textBPMColor[1], Settings.programSettings.textBPMColor[2])
    oldpos = cr.get_current_point()
    cr.move_to(Settings.programSettings.cover.SizeOfLongestTitle()*Settings.programSettings.textSize-0.8, oldpos[1])
    if 'BPM' in audio:
        cr.show_text(audio['BPM'][0])

#Run through the list of file, and call displayTrack for each one of them. Then render the cairo context to png and clear the fileList
def generateCover():
    global ctx, surface
    i=1
    for file in Settings.programSettings.cover.fileList:
        displayTrack(ctx, file, i)
        i += 1
    surface.write_to_png ("example.png")
    Settings.programSettings.cover.fileList.clear()

#Ask the user for the path to a file, and add it to the fileList stored in a settings object
def getPathFile() :
    temp = []
    temp.append(filedialog.askopenfilename())
    Settings.programSettings.cover.fileList = temp
    print(Settings.programSettings.cover.fileList)

#This function does 2 things : 1) it ask the user for a path, and look for every mp3 file in it and store the path to each one of them in a settings object
#                              2) given a path to a directory in argument, it does the same thing as 1) but using the path given as argument instead of asking the user for a path
def getPathDir(**kwargs) :
    if len(kwargs)>=1:
        for key, value in kwargs.items():
            if key == 'dir':
                relevant_path = value
            else :
                raise SyntaxError("Expected a directory")
    else:
        relevant_path = filedialog.askdirectory()

    print(relevant_path)
    pathList = []
    if relevant_path:
        included_extenstions = ['mp3']
        for fn in os.listdir(relevant_path):
            if any(fn.endswith(ext) for ext in included_extenstions):
                pathList.append(relevant_path +"/"+ fn)
                pathList = sorted(pathList)
    Settings.programSettings.cover.fileList = pathList

#Regenerate the ini before quitting the python script
def saveSettingsAndQuit():
    Settings.programSettings.regenerateIni()
    sys.exit(0)

#Simply quit the python script
def  quitWithoutSaving():
    sys.exit(0)

#A dialog that open on clicking on the "quit" button wich will ask the user if he want or not to the save his settings
def quitDialog():
        window = tkinter.Toplevel()
        dialog = tkinter.Label(window, text="Save settings before quitting ?")
        dialog.pack()
        yes = tkinter.Button(window, text="Yes", command=saveSettingsAndQuit)
        yes.pack()
        no = tkinter.Button(window, text="No", command=quitWithoutSaving)
        no.pack()

# --------- Cairo stuff --------- #

width = 1024
height = 1024
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

ctx = cairo.Context(surface)
ctx.scale(width, height) # Normalizing the canvas
ctx.set_source_rgb(0.98,0.98,0.98)
ctx.paint()

# --------- GUI --------- #

#Setting up the main program frame

args = parser.parse_args()
if len(sys.argv)>1:
    if args.file is not None:
        print("je passe")
        if os.path.exists(args.file) and os.path.isfile(args.file):
            print("Executing the script on the file :" + args.file)
            Settings.programSettings.cover.fileList = [args.file]
        else:
            raise FileNotFoundError('Invalid file specified')

    if args.directory is not None and not len(Settings.programSettings.cover.fileList) > 1:
        # special path formated specially for os.path.[...] to work
        args.directory = ' '.join(args.directory)
        osDir = args.directory.replace("\\", "")
        if os.path.exists(osDir) and os.path.isdir(osDir):
            print("Executing the script on the directory :" + args.directory)
            getPathDir(dir=args.directory)
        else:
            raise FileNotFoundError("Invalid directory specified")
    generateCover()
else:
    Settings.programSettings.parseIniFile()
    top = tkinter.Tk()
    top.resizable(width=False, height=False)
    top.winfo_height()
    top.wm_title(string="CoverGenerator 0.1")
    top.wm_minsize(500,500)

    #The "Generate Cover" button. It calls the generateCover function on click
    run = tkinter.Button(top,text = "Generate Cover", command = generateCover)
    run.pack()

    browseFile = tkinter.Button(top, text = "Browse a file", command = getPathFile)
    browseFile.pack()

    browseDir = tkinter.Button(top, text = "Browse a directory", command = getPathDir)
    browseDir.pack()

    pickColor = tkinter.Button(top, text = "Pick a color for the BPM", command=pickBPMColor)
    pickColor.pack()

    #saveSettings = tkinter.Button(top, text="Save settings", command=saveSettings)
    #saveSettings.pack()

    quitDialog = tkinter.Button(top, text="Quit", command=quitDialog)
    quitDialog.pack()

    top.mainloop()
