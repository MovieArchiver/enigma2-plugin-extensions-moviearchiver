# -*- coding: UTF-8 -*-
#######################################################################
#
#    MovieArchiver
#    Copyright (C) 2013 by svox
#    Code pieces from EnhancedMovieCenter by Copyright (C) 2011 by Coolman & Swiss-MAD
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

from time import time
from pipes import quote
from _collections import deque
from enigma import eConsoleAppContainer
import NavigationInstance
from Tools import Notifications
from Screens.MessageBox import MessageBox

from Components.config import config
from DiskUtils import pathIsWriteable, reachedLimit, getFiles, checkReachedLimitIfMoveFile, mountpoint
from . import printToConsole


# if in x secs a record starts, dont archive movies
SECONDS_NEXT_RECORD = 600 #10 mins

# max tries (movies to move) after checkFreespace recursion will end
MAX_TRIES = 30
MOVIE_EXTENSION_TO_ARCHIVE = ".ts"

class MovieManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.moveCommand = ""
        self.executionQueueList = deque()
        self.console = eConsoleAppContainer()
        self.console.appClosed.append(self.runFinished)

    def checkFreespace(self):
        tries = 0
        moviesFileSize = 0
        breakMoveNext = False

        if mountpoint(config.plugins.MovieArchiver.sourcePath.value) == mountpoint(config.plugins.MovieArchiver.targetPath.value):
            printToConsole("Stop archiving!! Can't archive movies to the same hard drive!! Please change the paths in the MovieArchiver settings")
            return

        if config.plugins.MovieArchiver.skipDuringRecords.value and self.isRecordingStartInNextTime():
            printToConsole("Skip archiving. A record is running or start in the next minutes.")
            return

        if reachedLimit(config.plugins.MovieArchiver.targetPath.value, config.plugins.MovieArchiver.targetLimit.value):
            if config.plugins.MovieArchiver.showLimitReachedNotification.value:
                Notifications.AddNotification(MessageBox, _("Stop archiving! Can't archive movie because archive-harddisk limit reached!\n"), type=MessageBox.TYPE_INFO, timeout=20)

            printToConsole("Stop archiving! Can't archive movie because archive-harddisk limit reached!")
            return

        if(reachedLimit(config.plugins.MovieArchiver.sourcePath.value, config.plugins.MovieArchiver.sourceLimit.value) and not reachedLimit(config.plugins.MovieArchiver.targetPath.value, config.plugins.MovieArchiver.targetLimit.value)):
            files = getFiles(config.plugins.MovieArchiver.sourcePath.value, MOVIE_EXTENSION_TO_ARCHIVE)
            if files is not None:
                for file in files:
                    moviesFileSize += os.path.getsize(file) / 1024 / 1024

                    # check if its enough that we move only this file
                    breakMoveNext = checkReachedLimitIfMoveFile(config.plugins.MovieArchiver.sourcePath.value, config.plugins.MovieArchiver.sourceLimit.value, moviesFileSize)

                    self.addMovieToArchiveQue(file)

                    if breakMoveNext or tries > MAX_TRIES:
                        break

                    tries += 1

                self.execQueue()
        else:
            printToConsole("limit not reached. Wait for next Event.")

    def addMovieToArchiveQue(self, sourceMovie):
        targetPath = config.plugins.MovieArchiver.targetPath.value
        if os.path.isdir(targetPath) and os.path.dirname(sourceMovie) != targetPath and pathIsWriteable(targetPath):
            fileNameWithoutExtension = os.path.splitext(sourceMovie)[0]
            newMoveCommand = 'mv "'+ fileNameWithoutExtension +'."* "'+ targetPath +'"'

            # add only if movie isnt in Queue
            if self.moveCommand != newMoveCommand and self.executionQueueList.count(newMoveCommand) == 0:
                self.executionQueueList.append(quote(newMoveCommand))

    def execQueue(self):
        try:
            if len(self.executionQueueList) > 0:
                self.moveCommand = self.executionQueueList.popleft()

                self.console.execute("sh -c " + self.moveCommand)

                printToConsole("execQueue: Move Movie '" + self.moveCommand + "'")
        except Exception, e:
            printToConsole("execQueue exception:\n" + str(e))

    def runFinished(self, retval=None):
        try:
            printToConsole("runFinished: sh exec %s, return status = %s" %(self.moveCommand, str(retval)))

            self.moveCommand = ""

            if len(self.executionQueueList) > 0:
                self.execQueue()
            else:
                printToConsole("Queue finished!")

        except Exception, e:
            printToConsole("runFinished exception:\n" + str(e))

            self.moveCommand = ""

            self.executionQueueList = deque()

    def isRecordingStartInNextTime(self):
        recordings = len(NavigationInstance.instance.getRecordings())
        nextRecordingTime = NavigationInstance.instance.RecordTimer.getNextRecordingTime()

        if not recordings and (((nextRecordingTime - time()) > SECONDS_NEXT_RECORD) or nextRecordingTime < 0):
            return False
        else:
            return True

