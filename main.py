import cairo, os, tkinter, json
from tkinter import filedialog, colorchooser
from mutagen.easyid3 import EasyID3

#test = "/home/paul/Music/test.mp3"
#testt2 = "/home/paul/Music/test2.mp3"

class settings:
    textSize = 0.015
    textBPMColor = (0.8, 0.4, 0.2)
    textBPMVerticalPos = 0.8
    configurationFile = "settings.ini"
    def __init__(self):
        self.textSize = 0.015
        self.textBPMColor = (0.8,0.4,0.2)
        self.textBPMVerticalPos =0.8
    @textBPMColor
    def getBPMColor(self):
        return self.textBPMColor
    @textSize
    def getTextSize(self):
        return self.textBPMColor
    @textBPMVerticalPos
    def getTextBPMVerticalOfffset(self):
        return self.textBPMVerticalPos

    @textBPMColor
    def setBPMColor(self, color):
        self.textBPMColor = color
    @textSize
    def setTextSize(self, size):
        self.textSize = size
    @textBPMVerticalPos
    def setTextBPMVerticalOffset(self, offset):
        self.textBPMVerticalPos = offset

    def createIniFile(self):
        execDirPath = os.path.dirname(__file__)
        print(execDirPath + "/" + self.configurationFile)
        ini = open(execDirPath + "/" + self.configurationFile, mode='a')
        ini.close()

    def createIni(self,pathToIni):
            with open(pathToIni, mode='w') as iniFile:
                json.dump({"color": cairoColorToTkColor(textBPMColor)}, iniFile)

    def parseIniFile(self,pathToIni):
            with open(pathToIni, mode='r') as iniFile:
                jsonSettings = json.load(iniFile)
                print(self.textBPMColor)
                self.setBPMColor(jsonSettings["color"])
                self.setBPMColor(TkColorToCairoColor(tuple(textBPMColor)))
                print(self.getBPMColor(textBPMColor))

class cover:
    fileList = []

programSettings = settings

def cairoColorToTkColor(color):
    result = []
    for i in color : result.append(int(i*255))
    return tuple(result)

def TkColorToCairoColor(color):
    result = []
    for i in color : result.append(i/255)
    return tuple(result)


def setBPMColor(color):
    global textBPMColor
    textBPMColor = (color[0], color[1], color[2])

def pickBPMColor():
    RGBColor = tkinter.colorchooser.askcolor(cairoColorToTkColor(textBPMColor))
    if (RGBColor):
        setBPMColor([RGBColor[0][0]/255, RGBColor[0][1]/255, RGBColor[0][2]/255])


def displayTrack(cr, trackname, tracknumber):
    audio = EasyID3(trackname)
    print(audio['title'])
    title = audio['title'][0]
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.select_font_face("Georgia",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(programSettings.textSize)
    ctx.move_to(0.05,(0.01+textPosVerticalOffset)*tracknumber+textPosTopOffset)
    ctx.show_text(title)
    ctx.set_source_rgb(textBPMColor[0], textBPMColor[1], textBPMColor[2])
    x_bearing, y_bearing, width, height = cr.text_extents(title)[:4]
    oldpos = ctx.get_current_point()
    ctx.move_to(textBPMVerticalPos,oldpos[1])
    ctx.show_text(audio['BPM'][0])

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

pickColor = tkinter.Button(top, text = "Pick a color for the BPM", command=pickBPMColor)
pickColor.pack()


top.mainloop()

