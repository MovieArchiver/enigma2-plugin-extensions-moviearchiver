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

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.config import config, configfile, getConfigListEntry, ConfigLocations
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText

from DiskUtils import pathIsWriteable
from NotificationController import NotificationController
from . import _, getSourcePath, getTargetPath
from ExcludeDirsView import ExcludeDirsView


#######################################################################

class MovieArchiverView(ConfigListScreen, Screen):
    skin = """
  <screen name="MovieArchiver-Setup" position="center,center" size="1000,440" flags="wfNoBorder" backgroundColor="#90000000">
    <eLabel name="new eLabel" position="0,0" zPosition="-2" size="630,440" backgroundColor="#20000000" transparent="0" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="37,405" size="250,33" text="Cancel" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="235,405" size="250,33" text="Save" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="442,405" size="250,33" text="Archive now!" transparent="1" />
    <widget name="config" position="21,74" size="590,300" scrollbarMode="showOnDemand" transparent="1" />
    <eLabel name="new eLabel" position="640,0" zPosition="-2" size="360,440" backgroundColor="#20000000" transparent="0" />
    <widget source="help" render="Label" position="660,74" size="320,400" font="Regular;20" />
    <eLabel position="660,15" size="360,50" text="Help" font="Regular; 40" valign="center" transparent="1" backgroundColor="#20000000" />
    <eLabel position="20,15" size="348,50" text="MovieArchiver" font="Regular; 40" valign="center" transparent="1" backgroundColor="#20000000" />
    <eLabel position="303,18" size="349,50" text="Setup" foregroundColor="unffffff" font="Regular; 30" valign="center" backgroundColor="#20000000" transparent="1" halign="left" />
    <eLabel position="425,400" size="5,40" backgroundColor="#e5dd00" />
    <eLabel position="220,400" size="5,40" backgroundColor="#61e500" />
    <eLabel position="20,400" size="5,40" backgroundColor="#e61700" />
    <eLabel text="by svox" position="42,8" size="540,25" zPosition="1" font="Regular; 15" halign="right" valign="top" backgroundColor="#20000000" transparent="1" />
  </screen>
"""

    def __init__(self, session, args = None):
        Screen.__init__(self, session)

        getSourcePath().addNotifier(self.checkReadWriteDir, initial_call=False, immediate_feedback=False)
        getTargetPath().addNotifier(self.checkReadWriteDir, initial_call=False, immediate_feedback=False)

        self.onChangedEntry = []

        ConfigListScreen.__init__(
            self,
            self.getMenuItemList(),
            session = session,
            on_change = self.__changedEntry
        )

        NotificationController.getInstance().setView(self)

        # Define Actions
        self["actions"] = ActionMap(["SetupActions", "OkCancelActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "save": self.save,
                "ok": self.ok,
                "yellow": self.yellow
            }, -2
        )

        self["config"].onSelectionChanged.append(self.__updateHelp)
        self["help"] = StaticText()

        self.onClose.append(self.__onClose)

    def getMenuItemList(self):
        menuList = []
        menuList.append(getConfigListEntry(_("Archive automatically"), config.plugins.MovieArchiver.enabled, _("If yes, the MovieArchiver automatically moved or copied (if 'Backup Movies' is on) movies to archive folder if limit is reached")))
        menuList.append(getConfigListEntry(_("Backup Movies instead of Archive"), config.plugins.MovieArchiver.backup, _("If yes, the movies will only be copy to the archive movie folder and not moved.\n\nCurrently for synchronize, it comparing only fileName and fileSize."), 'BACKUP'))
        menuList.append(getConfigListEntry(_("Skip archiving during records"), config.plugins.MovieArchiver.skipDuringRecords, _("If a record is in progress or start in the next minutes after a record, the archiver skipped till the next record")))
        menuList.append(getConfigListEntry(_("Show notification if archive limit reached"), config.plugins.MovieArchiver.showLimitReachedNotification, _("Show notification window message if 'Archive Movie Folder Limit' is reached")))
        menuList.append(getConfigListEntry(_("-------------------------------------------------------------"), ))
        menuList.append(getConfigListEntry(_("Movie Folder"), getSourcePath(), _("Source folder / HDD\n\nPress 'Ok' to open path selection view")))
        menuList.append(getConfigListEntry(_("Movie Folder Limit (in GB)"), config.plugins.MovieArchiver.sourceLimit, _("Movie Folder free diskspace limit in GB. If free diskspace reach under this limit, the MovieArchiver will move old records to the archive")))

        if config.plugins.MovieArchiver.backup.getValue() == True:
            menuList.append(getConfigListEntry(_("Exclude folders"),  config.plugins.MovieArchiver.excludeDirs, _("Selected Directories wont be backuped.")))

        menuList.append(getConfigListEntry(_("-------------------------------------------------------------"), ))
        menuList.append(getConfigListEntry(_("Archive Folder"), getTargetPath(), _("Target folder / HDD where the movies will moved or backuped.\n\nPress 'Ok' to open path selection view")))
        menuList.append(getConfigListEntry(_("Archive Folder Limit (in GB)"), config.plugins.MovieArchiver.targetLimit, _("If limit is reach, no movies will anymore moved to the archive")))

        return menuList

    # callback for path-browser
    def checkReadWriteDir(self, configElement):
        if pathIsWriteable(configElement.getValue()):
            configElement.lastValue = configElement.getValue()
            return True
        else:
            dirName = configElement.getValue()
            configElement.value = configElement.lastValue
            self.session.open(
                MessageBox,
                _("The directory %s is not writable.\nMake sure you select a writable directory instead.")%dirName,
                MessageBox.TYPE_ERROR
            )
            return False

    def yellow(self):
        NotificationController.getInstance().startArchiving(True)

    def excludedDirsChoosen(self, ret):
        config.plugins.MovieArchiver.excludeDirs.save()
        config.plugins.MovieArchiver.save()
        #config.save()

    def ok(self):
        cur = self.getCurrent()
        if cur == getSourcePath() or cur == getTargetPath():
            self.chooseDestination()
        elif cur == config.plugins.MovieArchiver.excludeDirs:
            self.session.openWithCallback(self.excludedDirsChoosen, ExcludeDirsView)
        else:
            ConfigListScreen.keyOK(self)

    def cancel(self):
        for x in self["config"].list:
            if len(x) > 1:
                x[1].cancel()
            else:
                pass

        self.close()

    def save(self):
        for x in self["config"].list:
            if len(x) > 1:
                # skip ConfigLocations because it doesnt accept default = None
                # All other forms override default and force to save values that
                # wasnt changed by user
                if isinstance(x[1], ConfigLocations) == False:
                    x[1].default = None
                x[1].save()
            else:
                pass

        if config.plugins.MovieArchiver.enabled.getValue():
            NotificationController.getInstance().start()
        else:
            NotificationController.getInstance().stop()

        configfile.save()
        self.close()

#############################################################

    def getCurrent(self):
        cur = self["config"].getCurrent()
        cur = cur and cur[1]
        return cur

    def pathSelected(self, res):
        if res is not None:
            pathInput = self.getCurrent()
            pathInput.setValue(res)

    def chooseDestination(self):
        from Screens.LocationBox import MovieLocationBox

        self.session.openWithCallback(
            self.pathSelected,
            MovieLocationBox,
            _("Choose folder"),
            self.getCurrent().getValue(),
            minFree = 100
        )


    '''
    Private Methods
    '''

    def __updateHelp(self):
        cur = self["config"].getCurrent()
        if cur:
            self["help"].text = cur[2]

    def __changedEntry(self):
        cur = self["config"].getCurrent()
        cur = cur and len(cur) > 3 and cur[3]
        # change if type is BACKUP
        if cur == "BACKUP":
            self["config"].setList(self.getMenuItemList())

    def __onClose(self):
        NotificationController.getInstance().setView(None)

