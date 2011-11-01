# -*- coding: utf-8 -*-
# $Id: Player.py 58 2008-01-02 07:46:26Z gassla $

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License version 2 or later'
__copyright__ = 'Copyright (c) 2007-2011 Thierry Randrianiriana'

import time
import copy
import random
import pygame
from const import *
from Board import Board
from Stone import Stone
from Utils import utils

class Player:
    """AI player class"""
    def __init__(self,board,color):
        self.color = color
        self.board = board

    def getColor(self):
        """return of the color of the AI player"""
        return self.color

    def getFreeStones(self):
        """return the list of the stones which can move ordered"""
        stones1 = []
        stones2 = []
        x = y = 0
        while x < self.board.cols :
            while y < self.board.rows :
                if self.board.stoneExists(x,y) :
                    stone = Stone(self.board , x,y)
                    if (stone.color == self.color or stone.color == utils.getSelectedColor(self.color) ) and stone.canMove() :
                        if stone.canBeCaptured() or x == 0 or (y + 1) == self.board.rows or y == 0 or (y + 1 ) == self.board.cols :
                            stones1.append((x,y))
                        else:
                            stones2.append((x,y) )
                y+=1
            x+=1
            y=0

        stones1 = utils.random_list(stones1)
        for a in stones2:
            stones1.append(a)

        return stones1

    def getSelectedStone(self):
        """return the stone selected by the AI"""
        result = []
        stones = self.getFreeStones()

        nb = 0
        for (x,y) in stones :
            stone = Stone(self.board,x,y)
            new_x , new_y , tmp_nb ,action = stone.canCaptureStones()
            if new_x >= 0 and new_y >= 0 and tmp_nb > nb :
                nb = tmp_nb
                result.insert(0, (x,y))

        if len(result) == 0 and len(stones) > 0 :
            #choose a stone randomly
            i = random.randint(0, len(stones) - 1 )
            result.append( stones[i] )

        return result[0]

    def update(self,screen):
        #FIXME on dirait que l'affichage est doublé avec ça
        self.board.populate_gui(screen)
        pygame.display.update()
	pygame.time.delay(DELAY)

    def play(self,screen):
        """the AI plays here"""
        must_choose = 0
        (ai_x, ai_y) = self.getSelectedStone()
#        print "AI x = %d y = %d " % (ai_x,ai_y)

        pStone = Stone(self.board , ai_x ,ai_y)
        pStone.selected()

        (new_x, new_y , nb , action) = pStone.canCaptureStones()
        if new_x >= 0 and new_y >= 0 :
            self.update(screen)

        timeout = 0
        while 1 :

            if timeout<10000:
                self.update(screen)
                timeout+=1

            (new_x, new_y , nb , action) = pStone.canCaptureStones()
            if new_x >= 0 and new_y >= 0 :

                timeout = 0

#                print "moves to (%d , %d)" % (new_x,new_y)
                if pStone.move(new_x,new_y) :
                    if pStone.mustChoose():
                        pStone.chooseAction(action)
                        pStone.selected()

                    if pStone.canMove() :
                        pStone.selected()

                    else :
#                         print "can't move and capture "
                        pStone.unselected()
                        break

            else :
                stones = self.getFreeStones()

                found = False
                for (sx,sy) in stones :
                    neib = utils.get_positions((sx,sy))


                    for (xx ,yy) in  neib:
                        oStone = Stone(self.board,sx,sy)

                        if xx>=0 and xx < self.board.cols and yy >=0 and yy < self.board.rows and oStone.legalMove(xx,yy) :
                            new_board = self.board.copy()
                            new_board.unselectedAll()

                            oStone = Stone(new_board,sx,sy)
                            if oStone.move(xx,yy):
                                if not oStone.canBeCaptured():
                                    found = True
                                    pStone = Stone(self.board , sx ,sy)
                                    pStone.selected()
                                    pStone.move(xx,yy)
                                    break

                    if found:
                        break

                if found:
                    break

                else:
                    print "must choose one"
                    neib = utils.get_positions((ai_x,ai_y))
                    oStone = Stone(self.board,ai_x,ai_y)
                    for (xx ,yy) in  neib:
                        if xx>=0 and xx < self.board.cols and yy >=0 and yy < self.board.rows and oStone.legalMove(xx,yy) :
                            found = True
                            pStone = Stone(self.board , sx ,sy)
                            pStone.selected()
                            pStone.move(xx,yy)
                            break
                    break


            self.board.unselectedAll()
            self.update(screen)
