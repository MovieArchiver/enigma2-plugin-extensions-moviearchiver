# -*- coding: UTF-8 -*-
#######################################################################
#
#    MovieArchiver
#    Copyright (C) 2013 by svox
#
#    In case of reuse of this source code please do not remove this copyright.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    For more information on the GNU General Public License see:
#    <http://www.gnu.org/licenses/>.
#
#######################################################################

import os
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.config import config
from Components.Sources.StaticText import StaticText
from Components.FileList import MultiFileSelectList
from DiskUtils import removeSymbolicLinks

from . import _, getSourcePathValue

#######################################################################

class ExcludeDirsView(Screen):
    skin = """
        <screen name="ExcludeDirsView" position="center,center" size="560,400" title="Select folders to exclude">
            <widget name="excludeDirList" position="5,0" size="550,320" transparent="1" scrollbarMode="showOnDemand" />
            <widget source="key_red" render="Label" font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="20,365" size="250,33" transparent="1" />
            <widget source="key_green" render="Label" font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="185,365" size="250,33" transparent="1" />
            <widget source="key_yellow" render="Label" font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="335,365" size="250,33" transparent="1" />
            <eLabel position="5,360" size="5,40" backgroundColor="#e61700" />
            <eLabel position="170,360" size="5,40" backgroundColor="#61e500" />
            <eLabel position="320,360" size="5,40" backgroundColor="#e5dd00" />
        </screen>"""


    def __init__(self, session):
        Screen.__init__(self, session)
        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("Save"))
        self["key_yellow"] = StaticText()

        self.excludedDirs = config.plugins.MovieArchiver.excludeDirs.getValue()
        self.dirList = MultiFileSelectList(self.excludedDirs, getSourcePathValue(), showFiles = False)
        self["excludeDirList"] = self.dirList

        self["actions"] = ActionMap(["DirectionActions", "OkCancelActions", "ShortcutActions"],
        {
            "cancel": self.exit,
            "red": self.exit,
            "yellow": self.changeSelectionState,
            "green": self.saveSelection,
            "ok": self.okClicked,
            "left": self.left,
            "right": self.right,
            "down": self.down,
            "up": self.up
        }, -1)
        if not self.selectionChanged in self["excludeDirList"].onSelectionChanged:
            self["excludeDirList"].onSelectionChanged.append(self.selectionChanged)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        idx = 0
        self["excludeDirList"].moveToIndex(idx)
        self.setWindowTitle()
        self.selectionChanged()

    def setWindowTitle(self):
        self.setTitle(_("Select Exclude Dirs"))

    def selectionChanged(self):
        current = self["excludeDirList"].getCurrent()[0]
        if current[2] is True:
            self["key_yellow"].setText(_("Deselect"))
        else:
            self["key_yellow"].setText(_("Select"))

    def up(self):
        self["excludeDirList"].up()

    def down(self):
        self["excludeDirList"].down()

    def left(self):
        self["excludeDirList"].pageUp()

    def right(self):
        self["excludeDirList"].pageDown()

    def changeSelectionState(self):
        self["excludeDirList"].changeSelectionState()
        self.excludedDirs = self["excludeDirList"].getSelectedList()

    def saveSelection(self):
        self.excludedDirs = self["excludeDirList"].getSelectedList()

        self.excludedDirs = removeSymbolicLinks(self.excludedDirs)

        config.plugins.MovieArchiver.excludeDirs.setValue(self.excludedDirs)
        config.plugins.MovieArchiver.excludeDirs.save()
        config.plugins.MovieArchiver.save()
        config.save()
        self.close(None)

    def exit(self):
        self.close(None)

    def okClicked(self):
        if self.dirList.canDescent():
            self.dirList.descent()
