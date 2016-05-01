import cairo, os, tkinter
from tkinter import filedialog, colorchooser
from mutagen.easyid3 import EasyID3

#test = "/home/paul/Music/test.mp3"
#test2 = "/home/paul/Music/test2.mp3"
textPosTopOffset = 0.1
textPosVerticalOffset = 0.05

textSize = 0.015
textBPMColor = (0.8,0.4,0.2)
textBPMVerticalPos = 0.8

fileList = []


def displayTrack(cr, trackname, tracknumber):
    audio = EasyID3(trackname)
    print(audio['title'])
    title = audio['title'][0]
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(textSize)
    ctx.move_to(0.05,(0.01+textPosVerticalOffset)*tracknumber+textPosTopOffset)
    ctx.show_text(title)
    ctx.set_source_rgb(textBPMColor[0], textBPMColor[1], textBPMColor[2])
    x_bearing, y_bearing, width, height = cr.text_extents(title)[:4]
    oldpos = ctx.get_current_point()
    ctx.move_to(textBPMVerticalPos,oldpos[1])
    #if (audio['BPM']):
    #    ctx.show_text(audio['BPM'][0])

def generateCover():
    i=1
    for file in fileList:
        displayTrack(ctx, file, i)
        i += 1
    surface.write_to_png ("example.png")
    fileList.clear()

def getPathFile() :
    global fileList
    fileList.append(filedialog.askopenfilename())
    print(fileList)

def getPathDir() :
    global fileList
    relevant_path = filedialog.askdirectory()
    if relevant_path:
        included_extenstions = ['mp3']
        for fn in os.listdir(relevant_path):
            if any(fn.endswith(ext) for ext in included_extenstions):
                fileList.append(relevant_path +"/"+ fn)


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


top.mainloop()

