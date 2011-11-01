#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id: setup.py 46 2007-10-22 06:10:53Z gassla $

import os
import glob

from distutils.core import setup
from os import listdir
from os.path import isdir, isfile

DESCRIPTION = """Fanorona"""
LONG_DESCRIPTION = """Fanorona a board game from Madagascar"""

CLASSIFIERS = [
    'License :: OSI-Approved Open Source :: GNU General Public License (GPL)',
    'Intended Audience :: by End-User Class :: End Users/Desktop',
    'Development Status :: 5 - Beta',
    'Topic :: Games/Entertainment :: Board Games',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Translations :: English',
    'Translations :: Malagasy',
    'Translations :: French',
]

# Packages
PACKAGES = ["fanorona", "fanorona.Utils"]

# Data
DATA_FILES = []

DATA_FILES.append( ('share/doc/fanorona', ['AUTHORS']) )
DATA_FILES.append( ('games', ['fanorona']) )
DATA_FILES.append(('share/games/fanorona/data', glob.glob('data/*.gif')))
DATA_FILES.append(('share/games/fanorona/data', glob.glob('data/*.png')))
DATA_FILES.append(('share/pixmaps/fanorona', glob.glob('data/icons/*.xpm')))
DATA_FILES.append( ('share/man/man6', ['manpages/fanorona.6']) )
DATA_FILES.append( ('share/applications', ['fanorona.desktop']) )

# Language
pofile = "LC_MESSAGES/fanorona"
for dir in [d for d in listdir("lang") if d.find(".svn") < 0 and isdir("lang/"+d)]:
    os.popen("msgfmt lang/%s/%s.po -o lang/%s/%s.mo" % (dir,pofile,dir,pofile))
    DATA_FILES.append( ("share/locale/"+dir+"/LC_MESSAGES", ["lang/"+dir+"/"+pofile+".mo"]) )

# Setup

setup (
    name             = 'fanorona',
    version          = "@VERSION@",
    classifiers      = CLASSIFIERS,
    description      = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author           = 'Thierry Randrianiriana',
    author_email     = 'randrianiriana@gmail.com',
    url              = 'http://home.gna.org/fanorona/',
    download_url     = 'http://download.gna.org/fanorona/',
    package_dir      = {'': 'lib'},
    packages         = PACKAGES,
    data_files       = DATA_FILES
)
