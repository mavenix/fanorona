# -*- coding: utf-8 -*-
# $Id: utils.py 55 2008-01-02 07:26:39Z gassla $

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License version 3'
__copyright__ = 'Copyright 2007-2011 Thierry Randrianiriana'

import time
import os
import random
import pygame
from fanorona.const import *
from gettext import gettext as _

def load_image(name):
	""" Load image and return image object"""

        dirname = os.path.join(BASE_DIR , 'data')
        if os.path.exists(dirname):
                fullname = os.path.join( dirname , name)
        else:
                fullname = os.path.join( 'data' , name)

	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
        	print 'Cannot load image:', fullname
        	raise SystemExit, message
	return image

def load_icon(name):
	""" Load image and return image object"""

        dirname = ICON_DIR
        if os.path.exists(dirname):
                fullname = os.path.join( dirname , name)
        else:
                fullname = os.path.join( 'data/icons' , name)

	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error, message:
        	print 'Cannot load image:', fullname
        	raise SystemExit, message
	return image

def invert_color(color):
	if color == BLACK :
		return RED
	else:
		return BLACK

def random_list(li):
	res = []

	if len(li) == 1 :
		return li

	while len(li)>0:
		i = random.randint(0, len(li) - 1 )
		res.append(li[i])
		li.pop(i)

	return res

def get_positions(pos):
	positions=[]
	(sx , sy ) = pos

	neib = [ (sx +1 , sy +1 ) , (sx , sy + 1 ) , (sx + 1 , sy ) , (sx + 1 , sy - 1 ) , (sx - 1 , sy +1 ) , (sx , sy - 1 )  , (sx - 1 , sy  ) , (sx - 1 , sy -1 ) ]

	neib = random_list(neib)

	for (xx ,yy) in  neib:
		if xx>=0 and yy>=0:
			if xx % 2 == yy % 2 and xx != 0 and yy != 0 and xx != 8 and yy != 4 :
				positions.insert(0 , (xx,yy))
			else:
				positions.insert(len(positions) , (xx,yy))

	return positions

def getSelectedColor(color):
        if color == WHITE:
		return SELECTED_WHITE
	return SELECTED_BLACK

def getColorName(color):
        if color == BLACK:
		return _("blue")
        elif color == WHITE:
		return _("red")
        else:
		return _("unknown")
