# -*- coding: utf-8 -*-

import os, os.path
import errno
from gettext import gettext as _

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License Version 3'
__copyright__ = 'Copyright 2007-2011 Thierry Randrianiriana'

BASE_DIR	= '/usr/share/games/fanorona/'
LOCALEDIR       = '/usr/share/locale'
ICON_DIR        = '/usr/share/pixmaps/fanorona/'
VERSION 	= '0.6'

DOMAIN 		= 'fanorona'

COPYRIGHT 	= _('Copyright 2007-2011 Thierry Randrianiriana')
DESCRIPTION   	= _('A board game from Madagascar')

if os.path.isfile('.fanorona_devel'):
    print '*** Using development data files ***'
    ICON_DIR = 'data/icons'
    LOCALEDIR = 'lang'

ICON_32 = "fanorona32x32.xpm"

EMPTY = 0
BLACK = 1
WHITE = 2
RED = WHITE
SELECTED_BLACK = 11
SELECTED_WHITE = 22

DELETE_PULL_BLACK = 81
DELETE_PULL_WHITE = 82

DELETE_PUSH_BLACK = 91
DELETE_PUSH_WHITE = 92

TIMEOUT = 60000 # ms
DELAY = 250 #ms refresh delay

#stone
BLACK_DELETE_STONE = "delete_blue.png"
RED_DELETE_STONE = "delete_red.png"

BLACK_STONE = "blue.png"
SELECTED_BLACK_STONE = "selected_blue.png"

RED_STONE = "red.png"
SELECTED_RED_STONE =  "selected_red.png"

STONE_SIZE = 35 #pixel
BOARD_BACKGROUND = "background.png"
STONE_SPACE = 50

# status
STATUS_RED = "status_red.png"
STATUS_BLACK = "status_blue.png"
STATUS_WHITE = "status_white.gif"
STATUS_DISABLED = "status_disabled.gif"

# command
PLAYER_PAUSE = "player_pause.png"
PLAYER_PLAY = "player_play.png"
PLAYER_END = "player_end.png"
PLAYER_STOP = "player_stop.png"
EXIT = "exit.png"
