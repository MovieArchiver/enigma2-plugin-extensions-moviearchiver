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
from Components.config import config, configfile, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from DiskUtils import pathIsWriteable
from NotificationController import NotificationController


#######################################################################

class MovieArchiverView(ConfigListScreen, Screen):
    skin = """
  <screen name="MovieArchiver-Setup" position="center,center" size="600,440" flags="wfNoBorder" backgroundColor="#90000000">
    <eLabel name="new eLabel" position="0,0" zPosition="-2" size="600,440" backgroundColor="#20000000" transparent="0" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="37,405" size="250,33" text="Cancel" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="235,405" size="250,33" text="Save" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="442,405" size="250,33" text="Archive now!" transparent="1" />
    <widget name="config" position="21,74" size="540,300" scrollbarMode="showOnDemand" transparent="1" />
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

        config.plugins.MovieArchiver.sourcePath.addNotifier(self.checkReadWriteDir, initial_call=False, immediate_feedback=False)
        config.plugins.MovieArchiver.targetPath.addNotifier(self.checkReadWriteDir, initial_call=False, immediate_feedback=False)

        ConfigListScreen.__init__(
            self,
            [
                getConfigListEntry(_("Enabled"), config.plugins.MovieArchiver.enabled),
                getConfigListEntry(_("-------------------------------------------------------------"), ),
                getConfigListEntry(_("Movie Folder"), config.plugins.MovieArchiver.sourcePath),
                getConfigListEntry(_("Movie Folder Limit (in GB)"), config.plugins.MovieArchiver.sourceLimit, _("Movie Folder free diskspace limit in GB. If free diskspace reach under this limit, the MovieArchiver will move old records to the archive")),
                getConfigListEntry(_("-------------------------------------------------------------"), ),
                getConfigListEntry(_("Archive Movie Folder"), config.plugins.MovieArchiver.targetPath),
                getConfigListEntry(_("Archive Movie Folder Limit (in GB)"), config.plugins.MovieArchiver.targetLimit, _("If limit is reach, no movies will anymore moved to the archive")),
            ],
            session = session,
            on_change = self.changed
        )

        # Define Actions
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "save": self.save,
                "ok": self.ok,
                "yellow": self.yellow
            }, -2
        )

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

    def changed(self):
        pass

    def ok(self):
        cur = self.getCurrent()
        if cur == config.plugins.MovieArchiver.sourcePath or cur == config.plugins.MovieArchiver.targetPath:
            self.chooseDestination()
        else:
            ConfigListScreen.keyOK(self)

    def yellow(self):
        NotificationController.getInstance().startArchiving()

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
                x[1].save()
            else:
                pass

        if config.plugins.MovieArchiver.enabled.value:
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
            pathInput.value = res

    def chooseDestination(self):
        from Screens.LocationBox import MovieLocationBox

        self.session.openWithCallback(
            self.pathSelected,
            MovieLocationBox,
            _("Choose folder"),
            self.getCurrent().value,
            minFree = 100 # Same requirement as in Screens.TimerEntry
        )

