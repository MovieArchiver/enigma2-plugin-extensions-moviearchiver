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

from Components.config import config
from DiskUtils import pathIsWriteable, reachedLimit, getFiles, checkReachedLimitIfMoveFile, mountpoint, getFilesWithNameKey, getFileHash
from EventDispatcher import dispatchEvent
from . import _, printToConsole, getSourcePathValue, getTargetPathValue

# Events
QUEUE_FINISHED = "queueFinished"

# if in x secs a record starts, dont archive movies
SECONDS_NEXT_RECORD = 600 #10 mins

# show message window: body is msg, timeout
INFO_MSG = "showAlert"

# max tries (movies to move) after checkFreespace recursion will end
MAX_TRIES = 30

# file extension to archive or backup
MOVIE_EXTENSION_TO_ARCHIVE = (".ts", ".avi", ".mkv", ".mp4", ".iso")

DEFAULT_EXCLUDED_DIRNAMES = [".Trash", "trashcan"]


class MovieManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.execCommand = ""
        self.executionQueueList = deque()
        self.console = eConsoleAppContainer()
        self.console.appClosed.append(self.__runFinished)

    def checkFreespace(self):
        if mountpoint(getSourcePathValue()) == mountpoint(getTargetPathValue()):
            dispatchEvent(INFO_MSG, _("Stop archiving!! Can't archive movies to the same hard drive!! Please change the paths in the MovieArchiver settings."), 10)
            return

        if config.plugins.MovieArchiver.skipDuringRecords.getValue() and self.isRecordingStartInNextTime():
            dispatchEvent(INFO_MSG, _("Skip archiving. A record is running or start in the next minutes."), 10)
            return

        if reachedLimit(getTargetPathValue(), config.plugins.MovieArchiver.targetLimit.getValue()):
            msg = _("Stop archiving! Can't archive movie because archive-harddisk limit reached!")

            printToConsole(msg)

            if config.plugins.MovieArchiver.showLimitReachedNotification.getValue():
                dispatchEvent(INFO_MSG, msg, 20)

            return

        if config.plugins.MovieArchiver.backup.getValue():
            self.backupFiles(getSourcePathValue(), getTargetPathValue())
        else:
            self.archiveMovies()

    def archiveMovies(self):
        '''
        archiving movies
        '''

        tries = 0
        moviesFileSize = 0

        if reachedLimit(getSourcePathValue(), config.plugins.MovieArchiver.sourceLimit.getValue()):
            files = getFiles(getSourcePathValue(), MOVIE_EXTENSION_TO_ARCHIVE)
            if files is not None:
                for file in files:
                    moviesFileSize += os.path.getsize(file) / 1024 / 1024

                    # Source Disk: check if its enough that we move only this file
                    breakMoveNext = checkReachedLimitIfMoveFile(getSourcePathValue(), config.plugins.MovieArchiver.sourceLimit.getValue(), moviesFileSize)

                    self.addMovieToArchiveQueue(file)

                    if breakMoveNext or tries > MAX_TRIES:
                        break

                    # Target Disk: check if limit is reached if we move this file
                    breakMoveNext = checkReachedLimitIfMoveFile(getTargetPathValue(), config.plugins.MovieArchiver.targetLimit.getValue(), moviesFileSize * -1)

                    if breakMoveNext:
                        break

                    tries += 1

                dispatchEvent(INFO_MSG, _("Start archiving."), 5)
                self.execQueue()
        else:
            dispatchEvent(INFO_MSG, _("limit not reached. Wait for next Event."), 5)

    def backupFiles(self, sourcePath, targetPath):
        '''
        sync files
        '''

        dispatchEvent(INFO_MSG, _("Backup Archive. Synchronization started"), 5)

        #check if target path is writable
        if pathIsWriteable(targetPath) == False:
            dispatchEvent(INFO_MSG, _("Backup Target Folder is not writable.\nPlease check the permission."), 10)
            return

        #check if some files to archive available
        sourceFiles = getFilesWithNameKey(sourcePath, excludedDirNames = DEFAULT_EXCLUDED_DIRNAMES, excludeDirs = config.plugins.MovieArchiver.excludeDirs.getValue())
        if sourceFiles is None:
            dispatchEvent(INFO_MSG, _("No files for backup found."), 10)
            return

        targetFiles = getFilesWithNameKey(targetPath, excludedDirNames = DEFAULT_EXCLUDED_DIRNAMES)

        # determine movies to sync and add to queue
        for sFileName,sFile in sourceFiles.iteritems():
            if sFileName not in targetFiles:
                printToConsole("file is new. Add To Archive: " + sFile)
                self.addFileToBackupQueue(sFile)
            else:
                tFile = targetFiles[sFileName]
                if getFileHash(tFile) != getFileHash(sFile):
                    printToConsole("file is different. Add to Archive: " + sFile)
                    self.addFileToBackupQueue(sFile)

        if len(self.executionQueueList) < 1:
            dispatchEvent(QUEUE_FINISHED, False)
        else:
            self.execQueue()

    def addFileToBackupQueue(self, sourceFile):
        targetPath = getTargetPathValue()
        if os.path.isdir(targetPath) and os.path.dirname(sourceFile) != targetPath and pathIsWriteable(targetPath):
            subFolderPath = sourceFile.replace(getSourcePathValue(), "")
            targetPathWithSubFolder = os.path.join(targetPath, subFolderPath)

            newExecCommand = 'cp "'+ sourceFile +'" "'+ targetPathWithSubFolder +'"'

            # create folders if doesnt exists
            folder = os.path.dirname(targetPathWithSubFolder)
            if os.path.exists(folder) == False:
                os.makedirs(folder)

            self.__addExecCommandToArchiveQueue(newExecCommand)

    def addMovieToArchiveQueue(self, sourceMovie):
        targetPath = getTargetPathValue()
        if os.path.isdir(targetPath) and os.path.dirname(sourceMovie) != targetPath and pathIsWriteable(targetPath):
            fileNameWithoutExtension = os.path.splitext(sourceMovie)[0]

            newExecCommand = 'mv "'+ fileNameWithoutExtension +'."* "'+ targetPath +'"'

            self.__addExecCommandToArchiveQueue(newExecCommand)

    def execQueue(self):
        try:
            if len(self.executionQueueList) > 0:
                self.execCommand = self.executionQueueList.popleft()

                self.console.execute("sh -c " + self.execCommand)

                printToConsole("execQueue: Move Movie '" + self.execCommand + "'")
        except Exception, e:
            printToConsole("execQueue exception:\n" + str(e))

    def isRecordingStartInNextTime(self):
        recordings = len(NavigationInstance.instance.getRecordings())
        nextRecordingTime = NavigationInstance.instance.RecordTimer.getNextRecordingTime()

        if not recordings and (((nextRecordingTime - time()) > SECONDS_NEXT_RECORD) or nextRecordingTime < 0):
            return False
        else:
            return True


    '''
    Private Methods
    '''

    def __runFinished(self, retval=None):
        try:
            self.execCommand = ""

            if len(self.executionQueueList) > 0:
                self.execQueue()
            else:
                printToConsole("Queue finished!")
                dispatchEvent(QUEUE_FINISHED, True)

        except Exception, e:
            printToConsole("runFinished exception:\n" + str(e))

            self.execCommand = ""

            self.executionQueueList = deque()

    def __addExecCommandToArchiveQueue(self, execCommandToAdd):
        '''
        add ExecCommand to executionQueueList if not in list
        '''
        #if self.execCommand != execCommandToAdd and self.executionQueueList.count(execCommandToAdd) == 0:
        if self.execCommand != execCommandToAdd and execCommandToAdd not in self.executionQueueList:
            self.executionQueueList.append(quote(execCommandToAdd))


