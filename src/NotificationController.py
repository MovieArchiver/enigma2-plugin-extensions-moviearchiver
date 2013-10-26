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

from Components.config import config
from MovieManager import MovieManager, QUEUE_FINISHED
from RecordNotification import RecordNotification, RECORD_FINISHED
from EventDispatcher import addEventListener, removeEventListener, hasEventListener
from Screens.MessageBox import MessageBox
from . import printToConsole
from Tools import Notifications

class NotificationController(object):
    '''
    classdocs
    '''
    instance = None

    def __init__(self):
        '''
        Constructor
        '''
        self.view = None
        self.movieManager = MovieManager()
        self.recordNotification = RecordNotification()

    @staticmethod
    def getInstance():
        if NotificationController.instance is None:
            NotificationController.instance = NotificationController()
        return NotificationController.instance

    def setView(self, view):
        self.view = view

    def getView(self):
        return self.view

    def start(self):
        if config.plugins.MovieArchiver.enabled.value:
            if self.recordNotification.isActive() == False:
                if hasEventListener(RECORD_FINISHED, self.__recordFinished) == False:
                    addEventListener(RECORD_FINISHED, self.__recordFinished)
                self.recordNotification.startTimer()

    def stop(self):
        removeEventListener(RECORD_FINISHED, self.__recordFinished)
        self.recordNotification.stopTimer()

    def startArchiving(self, showUIMessage = False):
        if showUIMessage == True:
            addEventListener(QUEUE_FINISHED, self.__queueFinished)
        else:
            removeEventListener(QUEUE_FINISHED, self.__queueFinished)

        try:
            self.movieManager.checkFreespace()
        except Exception, e:
            if showUIMessage == True:
                if e.args is not None and len(e.args) > 0:
                    # MessageBox.TYPE_ERROR
                    if len(e.args) > 1:
                        timeout = e.args[1]
                    else:
                        timeout = 10

                    self.showMessage(e.args[0], timeout)
                else:
                    printToConsole("startArchiving (yellow) Exception: " + str(e))
            else:
                printToConsole("startArchiving Exception: " + str(e))

    def showMessage(self, msg, timeout=10):
        if self.view is not None:
            self.view.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout)
        else:
            Notifications.AddNotification(MessageBox, msg, type=MessageBox.TYPE_INFO, timeout=timeout)

    '''
    Private Methods
    '''

    def __recordFinished(self):
        printToConsole("recordFinished")
        self.startArchiving()

    def __queueFinished(self, hasArchiveMovies):
        if hasArchiveMovies == True:
            self.showMessage(_("MovieArchiver: Archiving finished."), 5)
        else:
            self.showMessage(_("MovieArchiver: No movies to archive found."), 5)

