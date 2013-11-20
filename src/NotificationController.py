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
from MovieManager import MovieManager, QUEUE_FINISHED, INFO_MSG
from RecordNotification import RecordNotification, RECORD_FINISHED
from EventDispatcher import addEventListener, removeEventListener
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
        self.showUIMessage = None
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
        if config.plugins.MovieArchiver.enabled.value and self.recordNotification.isActive() == False:
            addEventListener(RECORD_FINISHED, self.__recordFinishedHandler)
            self.recordNotification.startTimer()

    def stop(self):
        removeEventListener(RECORD_FINISHED, self.__recordFinishedHandler)
        self.recordNotification.stopTimer()

    def startArchiving(self, showUIMessage = False):
        self.showUIMessage = showUIMessage

        if self.showUIMessage == True:
            addEventListener(QUEUE_FINISHED, self.__queueFinishedHandler)
        else:
            removeEventListener(QUEUE_FINISHED, self.__queueFinishedHandler)

        addEventListener(INFO_MSG, self.__infoMsgHandler)

        self.movieManager.startArchiving()

    def stopArchiving(self):
        self.movieManager.stopArchiving()
        self.showMessage(_("MovieArchiver: Stop Archiving."), 5)

    def isArchiving(self):
        '''
        returns true if currently archiving or backup is running
        '''
        return self.movieManager.running()


    def showMessage(self, msg, timeout=10):
        if self.view is not None:
            self.view.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout)
        else:
            Notifications.AddNotification(MessageBox, msg, type=MessageBox.TYPE_INFO, timeout=timeout)


    '''
    Private Methods
    '''

    def __recordFinishedHandler(self):
        printToConsole("recordFinished")
        self.startArchiving()

    def __queueFinishedHandler(self, hasArchiveMovies):
        if hasArchiveMovies == True:
            self.showMessage(_("MovieArchiver: Archiving finished."), 5)
        else:
            self.showMessage(_("MovieArchiver: Movies already archived."), 5)

    def __infoMsgHandler(self, msg, timeout = 10):
        if self.showUIMessage == True:
            self.showMessage(msg, timeout)
        else:
            printToConsole(msg)


