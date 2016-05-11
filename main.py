'''

(c) Paul Florence 2016

This file is part of Mp3CoverGenerator.
Mp3CoverGenerator is free software: you can redistribute it and / or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

Mp3CoverGenerator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar. If not, see < http://
    www.gnu.org / licenses / >.2
'''
import cairo, os, tkinter, json, Settings
from tkinter import filedialog, colorchooser
from mutagen.easyid3 import EasyID3

#test = "/home/paul/Music/test.mp3"
#testt2 = "/home/paul/Music/test2.mp3"


class cover:
    def __init__(self):
        self._fileList = []

    @property
    def fileList(self):
        return self._fileList


coverProperty = cover()

def pickBPMColor():
    RGBColor = tkinter.colorchooser.askcolor(Settings.cairoColorToTkColor(Settings.programSettings.textBPMColor))
    if (RGBColor):
        Settings.programSettings.textBPMColor = ([RGBColor[0][0]/255, RGBColor[0][1]/255, RGBColor[0][2]/255])


def displayTrack(cr, trackname, tracknumber):
    global ctx
    audio = EasyID3(trackname)
    print(audio['title'])
    title = audio['title'][0]

    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(Settings.programSettings.textSize)

    ctx.move_to(0.05,(0.01+Settings.programSettings.textVerticalOffset)*tracknumber+Settings.programSettings.textVerticalPos)
    ctx.show_text(title)

    ctx.set_source_rgb(Settings.programSettings.textBPMColor[0], Settings.programSettings.textBPMColor[1], Settings.programSettings.textBPMColor[2])

    oldpos = ctx.get_current_point()
    ctx.move_to(Settings.programSettings.textVerticalPos,oldpos[1])

    ctx.show_text(audio['BPM'][0])

def generateCover():
    global coverProperty, ctx
    i=1
    for file in coverProperty.fileList:
        displayTrack(ctx, file, i)
        i += 1
    surface.write_to_png ("example.png")
    coverProperty.fileList.clear()

def getPathFile() :
    global coverProperty
    coverProperty.fileList.append(filedialog.askopenfilename())
    print(coverProperty.fileList)

def getPathDir() :
    relevant_path = filedialog.askdirectory()
    if relevant_path:
        included_extenstions = ['mp3']
        for fn in os.listdir(relevant_path):
            if any(fn.endswith(ext) for ext in included_extenstions):
                coverProperty.fileList.append(relevant_path +"/"+ fn)


#audio['title'] = u"Example Title"
#audio['artist'] = u"Me"
#audio['album'] = u"My album"
#audio['composer'] = u"" # clear
#audio.save()

width = 1024
height = 1024
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context (surface)
ctx.scale (width, height) # Normalizing the canvas
ctx.set_source_rgb(0.98,0.98,0.98)
ctx.paint()
# --------- GUI --------- #

#Setting up the main program frame
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


top.mainloop()

