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

import json,os, tkinter
class settings:
    def __init__(self):
        self._textSize = 0.015
        self._textBPMColor = (0.8, 0.4, 0.2)
        self._textVerticalPos = 0.2
        self._textVerticalOffset = 0.05
        self.__configurationFile = os.path.dirname(__file__) + "/settings.ini"
        self._cover = cover()

    @property
    def textBPMColor(self):
        return self._textBPMColor
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

    @textBPMColor.setter
    def textBPMColor(self, color):
        self._textBPMColor = color
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

    def createIniFile(self):
        execDirPath = os.path.dirname(__file__)
        print(self.__configurationFile)
        ini = open(self.__configurationFile, mode='a')
        ini.close()

    def regenerateIni(self):
            with open(self.__configurationFile, mode='w') as iniFile:
                json.dump({"color": cairoColorToTkColor(self._textBPMColor),
                           "text size": self._textSize,
                           "fileList":self._cover.fileList}, iniFile)

            print("Saved settings to" + self.__configurationFile)

    def parseIniFile(self):
        self.createIniFile()
        if os.stat(self.__configurationFile).st_size > 0:
            print("Configuration file found, using it.")
            with open(self.__configurationFile, mode='r') as iniFile:
                if iniFile:
                    jsonSettings = json.load(iniFile)
                    self._textBPMColor = TkColorToCairoColor(jsonSettings["color"])
                    self._textSize = jsonSettings["text size"]
                    self._cover.fileList = jsonSettings["fileList"]
        else:
            print("No configuration file found, generating a new one for you.")
            self.regenerateIni()




def cairoColorToTkColor(color):
    result = []
    for i in color : result.append(int(i*255))
    return tuple(result)

def TkColorToCairoColor(color):
    result = []
    for i in color : result.append(i/255)
    return tuple(result)

class cover:
    def __init__(self):
        self._fileList = []

    @property
    def fileList(self):
        return self._fileList

    @fileList.setter
    def fileList(self, value):
        self._fileList = value

    def SizeOfLongestTitle(self):
        bestScore = 0
        for title in self.fileList:
            if len(title) > bestScore:
                bestScore = len(title)
        return bestScore
    def getWorkingData(self):
        prout = ["erer", "jeiv"]
        if len(self.fileList) != 1:
            return prout[0].rpartition("/")[0]
        else:
            return self.fileList[0]
    def toJson(self):
        return json.dump({"fileList": self._fileList})




programSettings = settings()