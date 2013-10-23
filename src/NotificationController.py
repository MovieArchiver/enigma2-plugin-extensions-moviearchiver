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
from MovieManager import MovieManager
from RecordNotification import RecordNotification, RECORD_FINISHED
from EventDispatcher import addEventListener, removeEventListener, hasEventListener
from . import printToConsole


class NotificationController(object):
    '''
    classdocs
    '''
    instance = None

    def __init__(self):
        '''
        Constructor
        '''
        self.movieManager = MovieManager()
        self.recordNotification = RecordNotification()

    @staticmethod
    def getInstance():
        if NotificationController.instance is None:
            NotificationController.instance = NotificationController()
        return NotificationController.instance

    def start(self):
        if config.plugins.MovieArchiver.enabled.value:
            if self.recordNotification.isActive() == False:
                if hasEventListener(RECORD_FINISHED, self.recordFinished) == False:
                    addEventListener(RECORD_FINISHED, self.recordFinished)
                self.recordNotification.startTimer()

    def stop(self):
        removeEventListener(RECORD_FINISHED, self.recordFinished)
        self.recordNotification.stopTimer()

    def recordFinished(self):
        printToConsole("recordFinished")
        self.startArchiving()

    def startArchiving(self):
        printToConsole("startArchiving")
        self.movieManager.checkFreespace()

