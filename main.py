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
import os, tkinter , json, Settings,cairo, argparse, sys
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from tkinter import filedialog, colorchooser

# --------- Argument parser --------- #

parser = argparse.ArgumentParser(description='Generate a cover from mp3 tag (and more)')
parser.add_argument('--file','-f', help="Pass a/some file(s) to process")
parser.add_argument('--directory','-d', help="Pass a directory to process", nargs='+')
parser.add_argument('--sort', '-s', help="Choose a sorting option, default: by alphabeletical order from the title field. Choose between: byTitle, byFilename, by tagNumber.")

# --------- Main Class --------- #

class Application :
    def __init__(self, width, height):
        self._settings = Settings.settings()
        self._tkTopLevel = tkinter.Tk()
        self._widgetList = list()
        self._cairoSurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self._ctx = cairo.Context(self._cairoSurface)
        self._width = width
        self._height = height
        self._redrawList = True

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
    #The main Tkinter llop
    def loop(self):
        self._tkTopLevel.mainloop()
    #Ask the user for a color and store so that it could be used as the drawn color for the BPM
    def pickBPMColor(self):
        RGBColor = colorchooser.askcolor(Settings.cairoColorToTkColor(self._settings._textBPMColor))
        if RGBColor[0]:
            self.settings.textBPMColor = ([RGBColor[0][0] / 255, RGBColor[0][1] / 255, RGBColor[0][2] / 255])

    # Add a track to the cairo context matchin the specified user input stored in a Settings object
    def displayTrack(self, trackname, tracknumber):
        #Specialization between the different audio format supported | TODO : Make this a function
        if trackname.rsplit(".")[-1] == "mp3":
            audio = EasyID3(trackname)
        else:
            if trackname.rsplit(".")[-1] == "flac":
                audio = FLAC(trackname)

        #Default space between different fields
        spacing = 0.05
        lastDrawnString = ""


        #Initializating cairo | TODO : Add the option to select the font
        self._ctx.set_source_rgb(0.0, 0.0, 0.0)
        self._ctx.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        self._ctx.set_font_size(self._settings.textSize)

        ###---/ Display the track number \---###
        if self.settings.displayNumber:
            number = str(tracknumber)
            self._ctx.move_to(0.01,(0.01 + self._settings.textVerticalOffset) * tracknumber + self._settings.textVerticalPos)
            self._ctx.show_text(number)
            lastDrawnString = number

        ###---/ Display the title \---###
        if 'title' in audio:
            title = audio['title'][0]
            self._ctx.move_to(spacing, (0.01 + self._settings.textVerticalOffset) * tracknumber + self._settings.textVerticalPos)
            self._ctx.show_text(title)
            lastDrawnString = title
        oldpos = self._ctx.get_current_point()

        ###---/ Display the artist \---###
        if self.settings.displayArtist and 'artist' in audio:
            self._ctx.set_source_rgb(self._settings.textArtistColor[0], self._settings.textArtistColor[1],self._settings.textArtistColor[2])
            artist = audio['artist'][0]
            self._ctx.move_to(self._settings.cover.SizeOfLongestTitle() * self._settings.textSize - 0.8, oldpos[1])
            self._ctx.show_text(artist)

        oldpos = self._ctx.get_current_point()
        self._ctx.move_to(oldpos[0] + spacing, oldpos[1])

        ###---/ Display the BPM\---###
        if 'BPM' in audio:
            self._ctx.set_source_rgb(self.settings.textBPMColor[0], self.settings.textBPMColor[1],
                                     self.settings.textBPMColor[2])
            self._ctx.show_text(audio['BPM'][0])

        oldpos = self._ctx.get_current_point()
        self._ctx.move_to(oldpos[0] + spacing, oldpos[1])
        ###---/ Display the Key\---###
        if 'initialkey' in audio:
            key = audio['initialkey'][0]
            color = self.settings.getKeyColor(key)
            self._ctx.set_source_rgb(color[0], color[1], color[2])
            self._ctx.show_text(key)


    # Run through the list of file, and call displayTrack for each one of them. Then render the cairo context to png and clear the fileList
    def generateCover(self):
        i = 1
        for file in self._settings.cover.fileList:
            self.displayTrack(file, i)
            i += 1
        self._cairoSurface.write_to_png("example.png")
        self._settings.cover.fileList = []
        print(str(self.settings.textBPMColor))

    # Ask the user for the path to a file, and add it to the fileList stored in a settings object
    def getPathFile(self):
        temp = []
        temp.append(filedialog.askopenfilename())
        self._settings.cover.fileList = temp
        print(self._settings.cover.fileList)
        self.updateOrderList()

    # This function does 2 things : 1) it ask the user for a path, and look for every mp3 file in it and store the path to each one of them in a settings object
    #                               2) given a path to a directory in argument, it does the same thing as 1) but using the path given as argument instead of asking the user for a path
    def getPathDir(self,**kwargs):
        self.settings.resetList()
        if len(kwargs) >= 1:
            for key, value in kwargs.items():
                if key == 'dir':
                    relevant_path = value
                else:
                    raise SyntaxError("Expected a directory")
        else:
            relevant_path = filedialog.askdirectory()
        print(relevant_path)
        pathList = []
        titleList = []
        if relevant_path:
            included_extenstions = ['mp3', 'flac']
            for fn in os.listdir(relevant_path):
                if any(fn.endswith(ext) for ext in included_extenstions):
                    pathList.append(relevant_path + "/" + fn)
                    pathList = sorted(pathList)
                    titleList.append(fn)
        self._settings.updateList(pathList)
        self.updateOrderList()


    # Regenerate the ini before quitting the python script
    def saveSettingsAndQuit(self):
        self._settings.regenerateIni()
        sys.exit(0)

    # Simply quit the python script
    def quitWithoutSaving(self):
        sys.exit(0)

    # A dialog that open on clicking on the "quit" button wich will ask the user if he want or not to the save his settings
    def exitDialog(self):
        window = tkinter.Toplevel()
        dialog = tkinter.Label(window, text="Save settings before quitting ?")
        window.wm_minsize(400,100)
        window.resizable(width=False, height=False)
        dialog.pack()
        yes = tkinter.Button(window, text="Yes", command=self.saveSettingsAndQuit)
        yes.place(height=40, relwidth=0.4, relx=0.25, rely=0.8, anchor="center")
        no = tkinter.Button(window, text="No", command=self.quitWithoutSaving)
        no.place(height=40, relwidth=0.4, relx=0.75, rely=0.8, anchor="center")

    def moveUp(self):
        selected = self._widgetList[-1].curselection()
        if selected > 1:
            self._settings.cover.permuteTitle(selected[0]-1, selected[0])
        self.updateOrderList()

    def moveDown(self):
        selected = self._widgetList[-1].curselection()
        if selected > 1:
            self._settings.cover.permuteTitle(selected[0] + 1, selected[0])
        self.updateOrderList()
        bleuh = self._settings.displayArtist
        print(bleuh)

    def updateOrderList(self):
        listBox = self._widgetList.pop()
        for index, track in enumerate(self._settings.cover.titleList):
            listBox.delete(index)
            listBox.insert(index, track)
        self._widgetList.append(listBox)

    def changeDisplayArtist(self):
        self.settings.displayArtist = (not self.settings.displayArtist)

    def changeDisplayTrackNumber(self):
        self.settings.displayNumber = (not self.settings.displayNumber)

    def initWidgets(self):
        #initialize all the cairo stuff
        self._ctx.scale(self._width, self._height)
        self._ctx.set_source_rgb(0.98,0.98,0.98)
        self._ctx.paint()

        self._settings.createIniFile()
        self._tkTopLevel.resizable(width=False, height=False)
        self._tkTopLevel.winfo_height()
        self._tkTopLevel.wm_title(string="CoverGenerator 0.1")
        self._tkTopLevel.wm_minsize(500, 500)

        self._settings.parseIniFile()

        # The "Generate Cover" button. It calls the generateCover function on click
        run = tkinter.Button(self._tkTopLevel, text="Generate Cover", command=self.generateCover)
        run.place(relwidth=0.6, relheight=0.15, relx=0.5, rely=0.92, anchor="center")
        self._widgetList.append(run)


        browseFile = tkinter.Button(self._tkTopLevel, text="Browse a file", command=self.getPathFile, )
        browseFile.place(relx=0.15, rely=0.05, relwidth=0.3, relheight=0.1, anchor="center")
        self._widgetList.append(browseFile)

        browseDir = tkinter.Button(self._tkTopLevel, text="Browse a directory", command=self.getPathDir)
        browseDir.place(relx=0.45, rely=0.05, relwidth=0.3, relheight=0.1, anchor="center")
        self._widgetList.append(browseDir)

        pickColor = tkinter.Button(self._tkTopLevel, text="Pick a color for the BPM", command=self.pickBPMColor)
        pickColor.place(relx=0.8, rely=0.05, relwidth=0.4, relheight=0.1, anchor="center")
        self._widgetList.append(pickColor)

        # saveSettings = tkinter.Button(self._tkTopLevel, text="Save settings", command=saveSettings)
        # saveSettings.pack()

        quitDialog = tkinter.Button(self._tkTopLevel, text="Quit", command=self.exitDialog)
        quitDialog.place(relwidth=0.2, relheight=0.15, relx=0.9, rely=0.92, anchor="center")
        self._widgetList.append(quitDialog)

        moveUp = tkinter.Button(self._tkTopLevel, text="Up", command=self.moveUp)
        moveUp.place(relx=0.6, rely=0.6,anchor="n")
        self._widgetList.append(moveUp)

        moveDown = tkinter.Button(self._tkTopLevel, text="Down", command=self.moveDown)
        moveDown.place(relx=0.3, rely=0.6,anchor="n"
                       )
        self._widgetList.append(moveDown)

        displayArtist = tkinter.Checkbutton(self._tkTopLevel, text="Display artist", command=self.changeDisplayArtist)
        displayArtist.place(relx = 0.2, rely=0.8)

        displayTrackNumber = tkinter.Checkbutton(self._tkTopLevel, text="Display track number", command=self.changeDisplayTrackNumber)
        displayTrackNumber.place(relx = 0.2, rely=0.75)

        #This should be the last item in the list ALWAYS
        orderList = tkinter.Listbox(self._tkTopLevel, selectmode = "Browse", width=30)
        for index, track in enumerate(self._settings.cover.titleList):
            orderList.insert(index, track)
            print(track)
        orderList.place(relx=0.5, rely=0.4,relwidth=0.9, anchor="center" )
        self._widgetList.append(orderList)

        if self._settings.displayArtist:
            displayArtist.select()
        if self._settings.displayNumber:
            displayTrackNumber.select()

# --------- GUI --------- #

#Setting up the main program frame

app = Application(1024, 1024)
app.initWidgets()
args = parser.parse_args()

if len(sys.argv)>1:
    app.settings.updateList([])
    app.updateOrderList()
    if args.file is not None:
        if os.path.exists(args.file) and os.path.isfile(args.file):
            print("Executing the script on the file :" + args.file)
            app.settings.updateList([args.file])
        else:
            raise FileNotFoundError('Invalid file specified')

    if args.directory is not None and not len(app.settings.cover.fileList) > 1:
        # special path formated specially for os.path.[...] to work
        args.directory = ' '.join(args.directory)
        osDir = args.directory.replace("\\", "")
        if os.path.exists(osDir) and os.path.isdir(osDir):
            print("Executing the script on the directory :" + args.directory)
            app.getPathDir(dir=args.directory)
        else:
            raise FileNotFoundError("Invalid directory specified")

app.loop()