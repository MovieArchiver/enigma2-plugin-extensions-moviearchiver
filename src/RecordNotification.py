# -*- coding: UTF-8 -*-
#######################################################################
#
#    MovieArchiver
#    Code by svox
#    Code pieces from PushService by betonme (c) 2012 <glaserfrank(at)gmail.com>
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#######################################################################

# Plugin specific
import NavigationInstance
from EventDispatcher import dispatchEvent
from enigma import eTimer
from . import printToConsole

# Event Types
RECORD_FINISHED = "recordFinished"

class RecordNotification():

	def __init__(self):
		self.forceBindRecordTimer = None

	def startTimer(self):
		self.forceBindRecordTimer = eTimer()
		self.forceBindRecordTimer.callback.append(self.begin)

		if self.isActive():
			self.forceBindRecordTimer.stop()

		self.forceBindRecordTimer.start(50, True)

		printToConsole("[RecordNotification] startTimer")

	def stopTimer(self):
		self.end()

		if self.forceBindRecordTimer is not None:
			self.forceBindRecordTimer.stop()
			self.forceBindRecordTimer.callback.remove(self.begin)
			self.forceBindRecordTimer = None

		printToConsole("[RecordNotification] stopTimer")

	def isActive(self):
		if self.forceBindRecordTimer is not None and self.forceBindRecordTimer.isActive():
			return True
		return False

	def begin(self):
		if NavigationInstance.instance:
			if self.onRecordEvent not in NavigationInstance.instance.RecordTimer.on_state_change:
				printToConsole("add RecordNotification")
				# Append callback function
				NavigationInstance.instance.RecordTimer.on_state_change.append(self.onRecordEvent)
		else:
			# Try again later
			self.forceBindRecordTimer.startLongTimer(1)

	def end(self):
		if NavigationInstance.instance:
			# Remove callback function
			if self.onRecordEvent in NavigationInstance.instance.RecordTimer.on_state_change:
				printToConsole("remove RecordNotification")
				NavigationInstance.instance.RecordTimer.on_state_change.remove(self.onRecordEvent)

	def onRecordEvent(self, timer):
		if timer.justplay:
			pass

		elif timer.state == timer.StatePrepared:
			pass

		elif timer.state == timer.StateRunning:
			pass

		# Finished repeating timer will report the state StateEnded+1 or StateWaiting
		elif timer.state == timer.StateEnded or timer.repeated and timer.state == timer.StateWaiting:
			printToConsole("[RecordNotification] record end!")
			dispatchEvent(RECORD_FINISHED)
			#del timer

