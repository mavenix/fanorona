# -*- coding: utf-8 -*-
# $Id: Board.py 58 2008-01-02 07:46:26Z gassla $

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License version 2 or later'
__copyright__ = 'Copyright 2007-2011 Thierry Randrianiriana'

import pygame
from numpy import *
from const import *
from fanorona.Utils import utils

class Board:
	"""This is the board class"""

	def __init__(self):
		self.rows = 5
		self.cols = 9
		self.matrix = zeros( (self.cols , self.rows ) )
		self.positions = {}

	def populate(self):
		x = y = 0
		while x < self.cols :
			while y < self.rows :
				if y < 2:
					self.matrix[x][y] = BLACK
				elif y > 2:
					self.matrix[x][y] = WHITE
				else:
					if x < 4 :
						if x % 2 == 0:
							self.matrix[x][y]= BLACK
						else :
							self.matrix[x][y]= WHITE
					elif x > 4 :
						if x % 2 != 0:
							self.matrix[x][y]= BLACK
						else :
							self.matrix[x][y]= WHITE

				y+=1
			x+=1
			y=0


	def getMatrix(self):
		return self.matrix

	def printMatrix(self):
		print self.matrix

	def show(self):
		mat = ""
		x = 0
		y = self.rows
		while y > 0  :
			y-=1
			while x < self.cols :
				mat = mat + '%d\t' % (self.matrix[x][y])
				x+=1
			x=0
			mat = mat + '\n\n\n\n'
		print mat

	def getStoneColor(self, x , y) :
		if self.stoneExists(x,y) :
			color = self.matrix[x][y]
			if color > 0:
				return color
			else:
				print "it's empty"

		return -1

	def stoneExists(self, x, y):
		if x < self.cols and x >= 0 and y < self.rows and y >= 0 :
			if self.matrix[x][y] > 0:
#				print "This stone (%d , %d ) exists" % (x , y)
				return True
# 		print "This stone (%d , %d ) doesn't exist" % (x , y)
		return False

	def populate_gui(self,screen):
		black = utils.load_image(BLACK_STONE)
		red = utils.load_image(RED_STONE)
		selected_black = utils.load_image(SELECTED_BLACK_STONE)
		selected_red = utils.load_image(SELECTED_RED_STONE)
		delete_black = utils.load_image(BLACK_DELETE_STONE)
		delete_red = utils.load_image(RED_DELETE_STONE)

		x = 0
		y = 0
		pos_y = ( self.rows * STONE_SPACE ) - (STONE_SIZE / 2)
		pos_x = STONE_SPACE - (STONE_SIZE / 2)

		while y < self.rows :
			while x < self.cols :
				if self.matrix[x][y] == BLACK :
					screen.blit(black, (pos_x, pos_y) )
				elif self.matrix[x][y] == WHITE :
					screen.blit(red , (pos_x, pos_y) )

				elif self.matrix[x][y] == SELECTED_WHITE :
					screen.blit(selected_red , (pos_x, pos_y) )

				elif self.matrix[x][y] == SELECTED_BLACK :
					screen.blit(selected_black , (pos_x, pos_y) )

				elif self.matrix[x][y] == DELETE_PULL_BLACK or self.matrix[x][y] == DELETE_PUSH_BLACK :
					screen.blit(delete_black , (pos_x, pos_y) )

				elif self.matrix[x][y] == DELETE_PULL_WHITE or self.matrix[x][y] == DELETE_PUSH_WHITE :
					screen.blit(delete_red , (pos_x, pos_y) )

				self.positions[(x,y)] = (pos_x + (STONE_SIZE /2) , pos_y + (STONE_SIZE /2))
				x+=1
				pos_x += STONE_SPACE

			y += 1
			pos_y = pos_y - STONE_SPACE

			x = 0
			pos_x = STONE_SPACE - (STONE_SIZE / 2)

		return screen

	def getSelectedPosition(self, mouse_position):
		(m_x , m_y) = mouse_position

		pass_round = False
		b_x , b_y = -1 , -1

		x = 0
		y = 0
		pos_y = self.rows * STONE_SPACE
		pos_x = STONE_SPACE

		if m_x < (STONE_SPACE - (STONE_SIZE / 2) ) or \
		       m_x > ((self.cols) * STONE_SPACE + (STONE_SIZE / 2) ) or \
		       m_y < (STONE_SPACE - (STONE_SIZE / 2) ) or \
		       m_y > ( self.rows * STONE_SPACE ) +  (STONE_SIZE / 2) :

			if m_x > (500-40) and m_y < 20:
				print "pass"
				pass_round = True
			else:
#				print "click out of the board"
				pass

		else :
			while y < self.rows  :
				if ( pos_y - (STONE_SIZE / 2) ) <= m_y and ( pos_y + (STONE_SIZE / 2) ) >= m_y :
					b_y = y

				pos_y = pos_y - STONE_SPACE

				while x < self.cols :
					if ( pos_x - (STONE_SIZE / 2) ) <= m_x and ( pos_x + (STONE_SIZE / 2) ) >= m_x :
						b_x = x

					x += 1

					pos_x += STONE_SPACE

				y += 1
				x = 0
				pos_x = STONE_SPACE

		return (b_x , b_y, pass_round)

	def unselectedAll(self):
		x = 0
		y = 0
		while y < self.rows  :
			while x < self.cols :
#				print "c : %d" % self.matrix[x][y]
				if self.matrix[x][y] == SELECTED_BLACK :
					self.matrix[x][y] = BLACK
				elif self.matrix[x][y] == SELECTED_WHITE :
					self.matrix[x][y] = WHITE
				x += 1
			y += 1
			x = 0

	def getSelectedStone(self):
		x = y = 0
		while y < self.rows  :
			while x < self.cols :
				if self.matrix[x][y] == SELECTED_BLACK :
					return (x,y,BLACK)
				elif self.matrix[x][y] == SELECTED_WHITE :
					return (x,y,WHITE)
				x += 1
			y += 1
			x = 0
		return (-1,-1,-1)

	def checkWinner(self):
		x = y = 0
		c = EMPTY
		while y < self.rows  :
			while x < self.cols :
				if self.matrix[x][y] != EMPTY and c == EMPTY :
					c = self.matrix[x][y]
				elif self.matrix[x][y] != EMPTY and self.matrix[x][y] != c :
					return None

				x += 1
			y += 1
			x = 0

		if c == BLACK:
			return BLACK
		else:
			return RED

	def isOn(self,xx,yy):
		if xx>=0 and xx < self.cols and yy >=0 and yy < self.rows:
			return True
		return False

	def copy(self):
		new_board = Board()
		new_board.positions = self.positions

		x = y = 0
		while x < self.cols :
			while y < self.rows :
				new_board.matrix[x][y] = self.matrix[x][y]
				y+=1
			x+=1
			y=0

		return new_board
