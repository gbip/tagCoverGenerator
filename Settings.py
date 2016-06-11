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

import json, os, cairo
from PIL import Image

# --------- Settings class --------- #
#A class representing the variable needed for the program to run. It his not really properly nammed (it contains other thing that just pure settings parameters).
class settings:
    # a dict with all keys and the matching RGB triplet color int the camelot wheel
    _keyColor = {'1A': (112, 239, 208), '2A': (146, 242, 159), '3A': (177, 244, 130), '4A': (228, 228, 165), '5A': (255, 198, 170),
                     '6A': (255, 175, 188), '7A': (255, 176, 208), '8A': (241, 176, 240), '9A': (229, 179, 255), '10A': (197, 209, 255),
                     '11A': (160, 230, 255), '12A': (112, 239, 208),
                     '1B': (0, 239, 202), '2B': (38, 240, 126), '3B': (129, 244, 67), '4B': (224, 203, 109), '5B': (255, 160, 121),
                     '6B': (255, 135, 147), '7B': (255, 127, 180), '8B': (241, 127, 220), '9B': (208, 139, 255), '10B': (158, 180, 255),
                     '11B': (76, 216, 250), '12B': (0, 234, 236)}

    def __init__(self):
        #the size of the text that will be displayed upon drawing the cover
        self._textSize = 0.015
        #the color of the BPM field
        self._textBPMColor = (0.8, 0.4, 0.2)
        #the color of the artist field
        self._textArtistColor = (0,0,0)
        #the position of the first line
        self._textVerticalPos = 0
        #the offset between 2 lines
        self._textVerticalOffset = 0.05
        #the absolute path to a configuration file
        self.__configurationFile = os.path.dirname(__file__) + "/settings.json"
        #a cover object (see the class cover)
        self._cover = cover()
        #should display the artist ?
        self._displayArtist = False
        #should display the track number ?
        self._displayTrackNumber = False
        #should display the key ?
        self._displayKey = False
        #path to save the cover
        self._coverPath = ""

    @property
    def textBPMColor(self):
        return self._textBPMColor
    @property
    def textArtistColor(self):
        return self._textArtistColor
    @property
    def textSize(self):
        return self._textSize
    @property
    def textVerticalPos(self):
        return self._textVerticalPos
    @property
    def textVerticalOffset(self):
        return self._textVerticalOffset
    @property
    def cover(self):
        return self._cover
    @property
    def displayArtist(self):
        return self._displayArtist
    @property
    def displayNumber(self):
        return self._displayTrackNumber
    @property
    def displayKey(self):
        return self._displayKey
    @property
    def outputPath(self):
        return self._coverPath

    @textBPMColor.setter
    def textBPMColor(self, color):
        self._textBPMColor = color
    @textArtistColor.setter
    def textArtistColor(self, value):
        self._textArtistColor = value
    @textSize.setter
    def textSize(self, size):
        self._textSize = size
    @textVerticalPos.setter
    def textVerticalPos(self, offset):
        self._textVerticalPos = offset
    @textVerticalOffset.setter
    def textVerticalOffset(self, offset):
        self._textVerticalOffset = offset
    @cover.setter
    def cover(self, newCover):
        self._cover = newCover
    @displayArtist.setter
    def displayArtist(self, value):
        self._displayArtist = value
    @displayNumber.setter
    def displayNumber(self, value):
        self._displayTrackNumber = value
    @displayKey.setter
    def displayKey(self, value):
        self._displayKey = value
    @outputPath.setter
    def outputPath(self, value):
        self._coverPath = value

    #Creat an empty .json file
    def createIniFile(self):
        execDirPath = os.path.dirname(__file__)
        print(self.__configurationFile)
        ini = open(self.__configurationFile, mode='a')
        ini.close()

    #Dump all the settings to an ini file in the form of a Json Object
    def regenerateIni(self):
            with open(self.__configurationFile, mode='w') as iniFile:
                json.dump({"BpmColor": cairoColorToTkColor(self._textBPMColor),
                           "ArtistColor": cairoColorToTkColor(self._textArtistColor),
                           "text size": self._textSize,
                           "fileList":self._cover.fileList,
                           "displayArtist": self._displayArtist,
                           "displayTrackNumber":self._displayTrackNumber,
                           "displayKey":self._displayKey,
                           "coverPath":self._coverPath}, iniFile)
            print("Saved settings to" + self.__configurationFile)

    #Look at the ini file and assign value to the settings object based on what is in the Json Object
    def parseIniFile(self):
        self.createIniFile()
        if os.stat(self.__configurationFile).st_size > 0:
            print("Configuration file found, using it.")
            with open(self.__configurationFile, mode='r') as iniFile:
                if iniFile:
                    jsonSettings = json.load(iniFile)
                    self._textBPMColor = TkColorToCairoColor(jsonSettings["BpmColor"])
                    self._textArtistColor = TkColorToCairoColor(jsonSettings["ArtistColor"])
                    self._textSize = jsonSettings["text size"]
                    self.updateList(jsonSettings["fileList"])
                    self._displayArtist = jsonSettings["displayArtist"]
                    self._displayTrackNumber = jsonSettings["displayTrackNumber"]
                    self._displayKey = jsonSettings["displayKey"]
                    self._coverPath = jsonSettings["coverPath"]
        else:
            print("No configuration file found, generating a new one for you.")
            self.regenerateIni()

    def updateList(self, pathList):
        self._cover.fileList = pathList
        for tracks in pathList:
            self._cover.titleList.append(tracks.rsplit("/")[-1])

    def resetList(self):
        self._cover.fileList.clear()
        self._cover.titleList.clear()

    def getKeyColor(self,key):
        return TkColorToCairoColor(self._keyColor[key])

    def generatekeyMapFile(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 32)
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()
        for index, key in enumerate(self._keyColor):
            color = TkColorToCairoColor(self._keyColor[key])
            ctx.set_source_rgb(color[0], color[1], color[2])
            ctx.rectangle((index) * 4, 0, 4, 8)
            ctx.fill()
            surface.write_to_png("key.png")

    def initalizeColorDictFromFile(self):
            im = Image.open("key.png")
            pixel = im.load()
            if im.size[0] == 96 and im.size[1] == 32:
                for index, key in enumerate(sorted(self._keyColor)):
                    color = pixel[index*4,2]
                    self._keyColor[key] = color
            else :
                print("Incorrect key file provided, should be 96*32")


#Convert color from cairo(value between 0 and 1) to Tk values (value between 0 and 255)
def cairoColorToTkColor(color):
    result = []
    for i in color : result.append(int(i*255))
    return tuple(result)

#Does the opposite of cairoColorToTkcolor(color)
def TkColorToCairoColor(color):
    result = []
    for i in color : result.append(i/255)
    return tuple(result)

# --------- Cover class --------- #
#a classe representing all the data needed to create a cover
class cover:
    def __init__(self):
        #A list of absolute path to the file that will be used to draw the cover
        self._fileList = list()
        self._titleList = list()

    @property
    def fileList(self):
        return self._fileList

    @property
    def titleList(self):
        return self._titleList

    @fileList.setter
    def fileList(self, value):
        self._fileList = value

    @titleList.setter
    def titleList(self, value):
        self.titleList = value

    #Return the size of the longuest title
    def longestFileName(self):
        bestScore = 0
        for title in self.fileList:
            if len(title) > bestScore:
                bestScore = len(title)
        return bestScore

    #Create a Json object from the cover object
    def toJson(self):
        return json.dump({"fileList": self._fileList})

    #Will permute 2 titles in the list (both the file list and the titleList
    def permuteTitle(self, index1, index2):
        backup = self.fileList[index1]
        backupTitle = self.titleList[index1]

        self.fileList[index1] = self.fileList[index2]
        self.titleList[index1] = self.titleList[index2]

        self.fileList[index2] = backup
        self.titleList[index2] = backupTitle