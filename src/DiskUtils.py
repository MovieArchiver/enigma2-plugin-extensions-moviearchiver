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

import os

###############################

def getOldestFile(path, fileExtension=None):
    '''
    get oldest file from folder

    fileExtensions example: .txt (with .)
    '''
    files = getFilesFromPath(path)

    if not files:
        return None

    if fileExtension is not None:
        files = filter(lambda s: s.endswith(fileExtension), files)

    oldestFile = min(files, key=os.path.getmtime)

    return oldestFile

def getFiles(path, fileExtension=None):
    '''
    get file list as an array
    sorted by date.
    The oldest first

    fileExtensions example: .txt (with .)
    '''
    files = getFilesFromPath(path)

    if not files:
        return None

    if fileExtension is not None:
        files = filter(lambda s: s.endswith(fileExtension), files)

    files.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
    return files

def getFilesFromPath(path):
    return [os.path.join(path, fname) for fname in os.listdir(path)]

def pathIsWriteable(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    if os.path.isdir(path) and ismount(path) and os.access(path, os.W_OK):
        return True
    else:
        return False

def ismount(path):
    return os.path.isdir(mountpoint(path))

def mountpoint(path, first=True):
    if first: path = os.path.realpath(path)
    if os.path.ismount(path) or len(path)==0: return path
    return mountpoint(os.path.dirname(path), False)

###############################

def getFreeDiskspace(path):
    # Check free space on path
    if os.path.exists(path):
        stat = os.statvfs(path)
        free = (stat.f_bavail if stat.f_bavail!=0 else stat.f_bfree) * stat.f_bsize / 1024 / 1024 # MB
        return free
    return 0 #maybe call exception

def getFreeDiskspaceText(path):
    free = getFreeDiskspace(path)
    if free >= 10*1024:    #MB
        free = "%d GB" %(free/1024)
    else:
        free = "%d MB" %(free)
    return free

def reachedLimit(path, limit):
    free = getFreeDiskspace(path)
    if limit > (free/1024): #GB
        return True
    else:
        return False

def checkReachedLimitIfMoveFile(path, limit, moviesFileSize):
    sourceHddFreeSpace = getFreeDiskspace(path)
    limitInMB = limit * 1024
    # Debug Code
    #print "[MovieArchiver] reachedLimitIfMoveFile sourceHddFreeSpace: " + str(sourceHddFreeSpace) + " moviesFileSize: " + str(moviesFileSize) + " limitInMB: " + str(limitInMB) + " ## " + str(sourceHddFreeSpace + moviesFileSize)
    if (sourceHddFreeSpace + moviesFileSize) >= limitInMB:
        return True
    else:
        return False


###############################
