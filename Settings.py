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

import json, os
class settings:
    configurationFile = "settings.ini"
    def __init__(self):
        self._textSize = 0.015
        self._textBPMColor = (0.8,0.4,0.2)
        self._textVerticalPos = 0.8
        self._textVerticalOffset = 0.05

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

    def createIniFile(self):
        execDirPath = os.path.dirname(__file__)
        print(execDirPath + "/" + self._configurationFile)
        ini = open(execDirPath + "/" + self._configurationFile, mode='a')
        ini.close()

    def createIni(self,pathToIni):
            with open(pathToIni, mode='w') as iniFile:
                json.dump({"color": cairoColorToTkColor(_textBPMColor)}, iniFile)

    def parseIniFile(self,pathToIni):
            with open(pathToIni, mode='r') as iniFile:
                jsonSettings = json.load(iniFile)
                print(self.textBPMColor)
                self.setBPMColor(jsonSettings["color"])
                self.setBPMColor(TkColorToCairoColor(tuple(_textBPMColor)))
                print(self.getBPMColor(_textBPMColor))

def cairoColorToTkColor(color):
    result = []
    for i in color : result.append(int(i*255))
    return tuple(result)

def TkColorToCairoColor(color):
    result = []
    for i in color : result.append(i/255)
    return tuple(result)

programSettings = settings()