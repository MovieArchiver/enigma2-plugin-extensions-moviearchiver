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


def getOldestFile(path, fileExtensions=None):
    '''
    get oldest file from folder

    fileExtensions as tuple. example: ('.txt', '.png')
    '''
    files = getFilesFromPath(path)

    if not files:
        return None

    files = __filterFileListByFileExtension(files, fileExtensions)

    oldestFile = min(files, key=os.path.getmtime)

    return oldestFile

def getFiles(path, fileExtensions=None):
    '''
    get file list as an array
    sorted by date.
    The oldest first

    fileExtensions as tuple. example: ('.txt', '.png')
    '''
    files = getFilesFromPath(path)

    if not files:
        return None

    files = __filterFileListByFileExtension(files, fileExtensions)

    files.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
    return files

def getFilesFromPath(path):
    return [os.path.join(path, fname) for fname in os.listdir(path)]

def getFilesWithNameKey(path):
    rs = {}
    for fileName in os.listdir(path):
        file = os.path.join(path, fileName)
        if os.path.isfile(file):
            rs[fileName] = file
    return rs

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

def getFileHash(file, factor=10, sizeToSkip=104857600):
    '''
    factor, if size is higher, it is faster but need more ram
    sizeToSkip 104857600 = 100mb
    '''
    # currently, we check only the fileSize because opening
    # files and creating hash are to slow
    return str(os.stat(file).st_size)

    '''
    filehash = hashlib.md5()

    # this size will stored in ram. and not the whole file
    blockSizeToRead = filehash.block_size * (2**factor)

    # we only want this 5mb for creating an md5 string
    sizeToRead = 5242880

    f = open(file, 'rb')
    f.seek(sizeToSkip, 0)

    totalSize = 0
    while (True):
        readData = f.read(blockSizeToRead)

        if not readData:
            if totalSize == 0:
                f.seek(0, 0)
                continue
            else:
                break

        totalSize += blockSizeToRead

        if totalSize > sizeToRead:
            break

        filehash.update(readData)

    hashStr = filehash.hexdigest()
    f.close()
    return hashStr
    '''


    '''
    Private Methods
    '''

def __filterFileListByFileExtension(files, fileExtensions):
    '''
    fileExtensions as tuple. example: ('.txt', '.png')
    '''
    if fileExtensions is not None:
        files = filter(lambda s: s.lower().endswith(fileExtensions), files)
        #files = filter(lambda s: s.endswith(fileExtension), files)
    return files
