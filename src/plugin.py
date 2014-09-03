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

from Plugins.Plugin import PluginDescriptor

import sys, traceback

from MovieArchiverView import MovieArchiverView
from NotificationController import NotificationController
from . import _, printToConsole

notificationController = None

#############################################################

# Autostart
def autostart(reason, **kwargs):
	global notificationController
	# Startup
	if reason == 0:
		try:
			notificationController = NotificationController.getInstance()
			notificationController.start()
		except Exception, e:
			printToConsole("Autostart exception " + str(e))
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)

	# Shutdown
	elif reason == 1:
		# Stop NotificationController
		if notificationController is not None:
			notificationController.stop()
			notificationController = None

#############################################################

def main(session, **kwargs):
	session.open(MovieArchiverView)

def Plugins(**kwargs):
	pluginList = [
		PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, fnc=autostart, needsRestart=False),
		PluginDescriptor(name="MovieArchiver", description=_("Archive or backup your movies"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main, needsRestart = False)
	]
	return pluginList
