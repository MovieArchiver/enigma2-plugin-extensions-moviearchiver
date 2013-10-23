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

handler = []

def hasEventListener(eventType, function):
    for e in handler:
        if e[0] == eventType and e[1] == function:
            return True
    return False

def addEventListener(eventType, function):
    handler.append([eventType, function])

def removeEventListener(eventType, function):
    for e in handler:
        if e[0] == eventType and e[1] == function:
            handler.remove(e)

def dispatchEvent(eventType, *arg):
    for e in handler:
        if e[0] == eventType:
            if(arg is not None and len(arg) > 0):
                e[1](*arg)
            else:
                e[1]()
