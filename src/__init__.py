
from Components.config import config, configfile, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigYesNo
from Tools.Directories import resolveFilename, SCOPE_HDD, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Screens.CCcamInfo import TranslationHelper

from os import environ
from Components.Language import language
import gettext, sys, traceback

#############################################################

# Gettext
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MovieArchiver", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "locale/"))

def _(txt):
    t = gettext.dgettext("MovieArchiver", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

def translateBlock(block):
    for x in TranslationHelper:
        if block.__contains__(x[0]):
            block = block.replace(x[0], x[1])
    return block

#############################################################

def printToConsole(msg):
    print "[MovieArchiver] " + msg

#############################################################

# Define Settings Entries
config.plugins.MovieArchiver = ConfigSubsection()
config.plugins.MovieArchiver.enabled = ConfigYesNo(default = False)
config.plugins.MovieArchiver.skipDuringRecords = ConfigYesNo(default = True)
config.plugins.MovieArchiver.showLimitReachedNotification = ConfigYesNo(default = True)

# default hdd
default = resolveFilename(SCOPE_HDD)
if config.movielist.videodirs.value and len(config.movielist.videodirs.value) > 0:
    default = config.movielist.videodirs.value[0]

config.plugins.MovieArchiver.sourcePath = ConfigText(default = default)
config.plugins.MovieArchiver.sourcePath.lastValue = config.plugins.MovieArchiver.sourcePath.value

config.plugins.MovieArchiver.sourceLimit = ConfigNumber(default=30)

config.plugins.MovieArchiver.targetPath = ConfigText(default = default)
config.plugins.MovieArchiver.targetPath.lastValue = config.plugins.MovieArchiver.targetPath.value

# interval
config.plugins.MovieArchiver.targetLimit = ConfigNumber(default=30)


#############################################################


__all__ = ['_', 'config']
