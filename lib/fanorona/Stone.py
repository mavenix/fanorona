# -*- coding: utf-8 -*-
# $Id: Stone.py 55 2008-01-02 07:26:39Z gassla $

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License version 3 or later'
__copyright__ = 'Copyright 2007-2011 Thierry Randrianiriana'

from const import *
from numpy import *
from Utils import utils

class Stone:
    def __init__(self, board , x , y) :
        self.x = self.y = self.color = -1
        if board.stoneExists(x,y) :
            self.x = x
            self.y = y
            self.color = board.getStoneColor(x,y)
            self.selected_color = utils.getSelectedColor(self.color)
            self.board = board
            self.history = {}

            self.historix = zeros( (self.board.cols , self.board.rows ) )

        else:
            print "Initialization failed"

    def getPosition(self):
        return self.x , self.y


    def getPositionOnBoard(self):
        if self.board.positions.has_key((self.x,self.y)):
            return self.board.positions[(self.x,self.y)]
        return (-1,-1)


    def getInfo(self):
        return self.x , self.y , self.color

    def getHistory(self):
        return self.history

    def move(self, new_x , new_y):
        nb = 0
        x, y = self.x , self.y

        if self.mustChoose():
            nb = self.choose(new_x,new_y)
            old_x, old_y = self.getLastPosition()
            self.history[(old_x, old_y)] = nb
            self.historix[old_x][old_y] = len(self.history)
            return True

        elif self.legalMove( new_x, new_y):
            (nb , action) = self.captureStones( new_x, new_y)
            self.history[(x, y)] = nb
            self.historix[x][y] = len(self.history)
            self.board.matrix[self.x][self.y] = EMPTY
            self.board.matrix[new_x][new_y] = self.color
            self.x , self.y = new_x , new_y
            return True
        return False

    def legalMove(self, new_x,new_y):
        can = False
        if not self.board.stoneExists(new_x,new_y) and not self.history.has_key((new_x,new_y)) :
            delta_x , delta_y = abs(self.x - new_x) , abs(self.y - new_y)
            if (delta_x == 0 or delta_x == 1) and (delta_y == 0 or delta_y == 1) :

                if self.x % 2 != self.y % 2 and delta_y + delta_x == 1 :
                    can = True
                elif (self.x % 2 == self.y % 2) and (delta_y + delta_x > 0) :
                    can = True

                if can and len(self.history)>0:
                    old_x , old_y = self.getLastPosition()
                    delta_old_x , delta_old_y = self.x - old_x , self.y - old_y

                    if self.history[(old_x,old_y)] == 0 :
#                        print "can't move if in the last action stone didn't capture stones"
                        can = False
                    elif  (self.y + delta_old_y) == new_y and (self.x + delta_old_x) == new_x :
#                        print "can't move in the same direction"
                        can = False
                    elif self.captureStones(new_x,new_y,0) == (0,'push') or self.captureStones(new_x,new_y,0) == (0,'pull') :
#                        print "can't move if the stone will not capture a stone"
                        can = False


#         if not can :
#             print "( %d , %d ) illegal move" % (new_x, new_y)

        return can

    def captureStones(self,new_x,new_y, real = 1) :
        delta_x , delta_y = new_x - self.x , new_y - self.y
        a = 0
        b = 0
        nb = 0
        action = "push"

        if self.x != new_x :
            a = delta_y / delta_x
            b = ((self.x * new_y ) - (self.y * new_x )) / (self.x - new_x)

        pushStones = self.pushStones(new_x,new_y)
        pullStones = self.pullStones(new_x,new_y)

        if len(pushStones)>0 and len(pullStones)>0 :
            if len(pushStones) > len(pullStones) :
                nb = len(pushStones)
                action = "push"
            else :
                nb = len(pullStones)
                action = "pull"

            if real == 0 :
                return (nb,action)

            for (xx , yy ) in pushStones:
                if self.color == BLACK :
                    self.board.matrix[xx][yy] = DELETE_PUSH_WHITE
                else:
                    self.board.matrix[xx][yy] = DELETE_PUSH_BLACK

            for (xx , yy ) in pullStones:
                if self.color == BLACK :
                    self.board.matrix[xx][yy] = DELETE_PULL_WHITE
                else:
                    self.board.matrix[xx][yy] = DELETE_PULL_BLACK

#             action = self.askAction()

#             if action == 'pull' :
#                 nb = self.removeStones(pullStones,real)
#             else:
#                 nb = self.removeStones(pushStones,real)

        elif len(pushStones)>0 and len(pullStones) == 0 :
            nb = self.removeStones(pushStones,real)
            action = "push"

        elif len(pullStones)>0 and len(pushStones) == 0 :
            nb = self.removeStones(pullStones,real)
            action = "pull"

        return (nb,action)

    def pullStones(self,new_x,new_y):
        stones = {}
	delta_x , delta_y = new_x - self.x , new_y - self.y

        sign_x = 1
        if delta_x != 0 :
            sign_x = delta_x / abs(delta_x)

        sign_y = 1
        if delta_y != 0 :
            sign_y = delta_y / abs(delta_y)

        i = 1
        while i < self.board.cols * self.board.rows :
            xx = self.x
            if delta_x != 0 :
                xx = self.x - (sign_x * i )

            yy = self.y
            if delta_y != 0 :
                yy = self.y - (sign_y * i)

            if xx >= self.board.cols or xx < 0 or yy >= self.board.rows or yy < 0 :
                break

#            print "pull (%d , %d)" % (xx,yy)
            cc=self.board.matrix[xx][yy]

            mycolor = self.color
            if mycolor == SELECTED_BLACK :
                mycolor = BLACK
            elif mycolor == SELECTED_WHITE :
                mycolor = WHITE

            if cc == EMPTY :
                break

            elif cc != mycolor :
                stones[(xx, yy)] = (xx,yy)

            else:
                break
            i+=1

        return stones

    def pushStones(self,new_x,new_y):
        stones = {}
	delta_x , delta_y = new_x - self.x , new_y - self.y

        sign_x = 1
        if delta_x != 0 :
            sign_x = delta_x / abs(delta_x)

        sign_y = 1
        if delta_y != 0 :
            sign_y = delta_y / abs(delta_y)

        i=1
        while i < (self.board.cols * self.board.rows) :
            xx = new_x
            if delta_x != 0 :
                xx = new_x + (sign_x * i )

            yy =  new_y
            if delta_y != 0 :
                yy = new_y + (sign_y * i)

            if xx >= self.board.cols or xx < 0 or yy >= self.board.rows or yy < 0 :
                break

#            print "push (%d , %d)" % (xx,yy)
            cc=self.board.matrix[xx][yy]

            mycolor = self.color
            if mycolor == SELECTED_BLACK :
                mycolor = BLACK
            elif mycolor == SELECTED_WHITE :
                mycolor = WHITE

            if cc == EMPTY :
                break

            elif cc != mycolor :
                stones[(xx, yy)] = (xx,yy)

            else:
                break

            i+=1

        return stones

    def removeStones(self, stones , real = 1 ):
        nb = 0
        for (xx , yy) in stones.keys():
            if real > 0 :
                self.board.matrix[xx][yy] = EMPTY
            nb += 1
        return nb

    def askAction(self):
        action = raw_input("Type 'pull' or 'push' (default): ")
        if action == 'pull' :
            return 'pull'
        else:
            return 'push'

    def canMove(self):
        neib = [ (self.x , self.y + 1 ) , (self.x +1 , self.y +1 ) , (self.x + 1 , self.y ) , (self.x + 1 , self.y - 1 ) , (self.x , self.y - 1 ) , (self.x - 1 , self.y -1 ), (self.x - 1 , self.y  ) , (self.x - 1 , self.y +1 ) ]

        for (xx ,yy) in neib:
            if xx>=0 and xx < self.board.cols and yy >=0 and yy < self.board.rows and self.legalMove(xx,yy) :
                return True

        return False

    def canCaptureStones(self):
        neib = [ (self.x , self.y + 1 ) , (self.x +1 , self.y +1 ) , (self.x + 1 , self.y ) , (self.x + 1 , self.y - 1 ) , (self.x , self.y - 1 ) , (self.x - 1 , self.y -1 ), (self.x - 1 , self.y  ) , (self.x - 1 , self.y +1 ) ]

        res = (-1,-1,0,'')
        nb = 0
        action = "push"
        for (xx ,yy) in neib:
            if xx>=0 and xx < self.board.cols and yy >=0 and yy < self.board.rows and self.legalMove(xx,yy) :
                (tmp_nb,tmp_action) = self.captureStones(xx,yy,0)
                if tmp_nb > nb :
                    nb = tmp_nb
                    action = tmp_action
                    res = (xx,yy,nb,action)

        return res

    def mustChoose(self):
        x = y = 0
        while x < self.board.cols :
            while y < self.board.rows :
                if self.board.matrix[x][y] == DELETE_PULL_WHITE or self.board.matrix[x][y] == DELETE_PUSH_WHITE or self.board.matrix[x][y] == DELETE_PULL_BLACK or self.board.matrix[x][y] == DELETE_PUSH_BLACK :
                    return True
                y+=1
            x+=1
            y=0
        return False

    def choose(self,xx,yy):
        nb = x = y =0

        if self.board.matrix[xx][yy] == DELETE_PULL_WHITE :
            while x < self.board.cols :
                while y < self.board.rows :
                    if self.board.matrix[x][y] == DELETE_PULL_WHITE :
                        self.board.matrix[x][y] = EMPTY
                        nb += 1
                    elif self.board.matrix[x][y] == DELETE_PUSH_WHITE :
                        self.board.matrix[x][y] = WHITE
                    y+=1
                x+=1
                y=0

        elif self.board.matrix[xx][yy] == DELETE_PUSH_WHITE :
            while x < self.board.cols :
                while y < self.board.rows :
                    if self.board.matrix[x][y] == DELETE_PUSH_WHITE :
                        self.board.matrix[x][y] = EMPTY
                        nb += 1
                    elif self.board.matrix[x][y] == DELETE_PULL_WHITE :
                        self.board.matrix[x][y] = WHITE
                    y+=1
                x+=1
                y=0

        elif self.board.matrix[xx][yy] == DELETE_PULL_BLACK :
            while x < self.board.cols :
                while y < self.board.rows :
                    if self.board.matrix[x][y] == DELETE_PULL_BLACK :
                        self.board.matrix[x][y] = EMPTY
                        nb += 1
                    elif self.board.matrix[x][y] == DELETE_PUSH_BLACK :
                        self.board.matrix[x][y] = BLACK
                    y+=1
                x+=1
                y=0

        elif self.board.matrix[xx][yy] == DELETE_PUSH_BLACK :
            while x < self.board.cols :
                while y < self.board.rows :
                    if self.board.matrix[x][y] == DELETE_PUSH_BLACK :
                        self.board.matrix[x][y] = EMPTY
                        nb += 1
                    elif self.board.matrix[x][y] == DELETE_PULL_BLACK :
                        self.board.matrix[x][y] = BLACK
                    y+=1
                x+=1
                y=0

        return nb

    def chooseAction(self,action):
        x = y = 0
        while x < self.board.cols :
            while y < self.board.rows :
                if action == "push":
                    if self.board.matrix[x][y] == DELETE_PUSH_WHITE or self.board.matrix[x][y] == DELETE_PUSH_BLACK :
                        self.board.matrix[x][y] = EMPTY
                    elif self.board.matrix[x][y] == DELETE_PULL_BLACK :
                        self.board.matrix[x][y] = BLACK
                    elif self.board.matrix[x][y] == DELETE_PULL_WHITE :
                        self.board.matrix[x][y] = WHITE

                elif action == "pull":
                    if self.board.matrix[x][y] == DELETE_PULL_WHITE or self.board.matrix[x][y] == DELETE_PULL_BLACK :
                        self.board.matrix[x][y] = EMPTY
                    elif self.board.matrix[x][y] == DELETE_PUSH_BLACK :
                        self.board.matrix[x][y] = BLACK
                    elif self.board.matrix[x][y] == DELETE_PUSH_WHITE :
                        self.board.matrix[x][y] = WHITE

                y+=1
            x+=1
            y=0


    def selected(self):
        self.board.unselectedAll()

        if self.color == BLACK:
            self.board.matrix[self.x][self.y] = SELECTED_BLACK
        elif self.color == WHITE:
            self.board.matrix[self.x][self.y] = SELECTED_WHITE

    def isSelected(self):
        if self.board.matrix[self.x][self.y] == SELECTED_BLACK or self.board.matrix[self.x][self.y] == SELECTED_WHITE :
            return True
        return False

    def unselected(self):
        if self.color == SELECTED_BLACK :
            self.board.matrix[self.x][self.y] = BLACK
        elif self.color == SELECTED_WHITE:
            self.board.matrix[self.x][self.y] = WHITE

    def getLastPosition(self):
        r_x = r_y = 0
        tmp = x = y = 0

	while x < self.board.cols :
		while y < self.board.rows :
                    if self.historix[x][y] > tmp:
                        tmp = self.historix[x][y]
                        r_x = x
                        r_y = y
                    y+=1
		x+=1
		y=0
        return (r_x , r_y )

    def canBeCaptured(self):
        self.board.unselectedAll()

        # x , y + 1
        if self.board.isOn(self.x,self.y + 1) and self.board.isOn(self.x,self.y + 2) :
            if (self.board.matrix[self.x][self.y + 1] == EMPTY and \
                self.board.matrix[self.x][self.y + 2] != self.color and \
                self.board.matrix[self.x][self.y + 2] != EMPTY) \
                or \
                   (self.board.matrix[self.x][self.y + 1] != self.color and \
                    self.board.matrix[self.x][self.y + 1] != EMPTY and \
                    self.board.matrix[self.x][self.y + 2] == EMPTY):
#                print "captured (x , y+1)= %d ; (x , y+2)=%d " % (self.board.matrix[self.x][self.y + 1],self.board.matrix[self.x][self.y + 2] )
                return True

        # x + 1 , y
        if self.board.isOn(self.x + 1,self.y) and self.board.isOn(self.x + 2,self.y) :
            if (self.board.matrix[self.x + 1][self.y] == EMPTY and \
                self.board.matrix[self.x + 2][self.y] != self.color and \
                self.board.matrix[self.x + 2][self.y] != EMPTY) \
                or \
                   (self.board.matrix[self.x + 1][self.y] != self.color and \
                    self.board.matrix[self.x + 1][self.y] != EMPTY and \
                    self.board.matrix[self.x + 2][self.y] == EMPTY):
#                print "captured (x +1 , y) = %d ; (x + 2 , y) = %d " % (self.board.matrix[self.x + 1][self.y] ,self.board.matrix[self.x + 2][self.y] )
                return True

        # x , y - 1
        if self.board.isOn(self.x,self.y - 1) and self.board.isOn(self.x,self.y - 2) :
            if (self.board.matrix[self.x][self.y - 1] == EMPTY and self.board.matrix[self.x][self.y - 2] != self.color) or \
                   (self.board.matrix[self.x][self.y - 1] != self.color and self.board.matrix[self.x][self.y - 2] == EMPTY):
#                print "captured (x , y - 1)"
                return True

        # x - 1 , y
        if self.board.isOn(self.x - 1,self.y) and self.board.isOn(self.x - 2,self.y) :
            if (self.board.matrix[self.x - 1][self.y] == EMPTY and \
                self.board.matrix[self.x - 2][self.y] != EMPTY and \
                self.board.matrix[self.x - 2][self.y] != self.color) \
                or \
                   (self.board.matrix[self.x - 1][self.y] != self.color and \
                    self.board.matrix[self.x - 1][self.y] != EMPTY and \
                    self.board.matrix[self.x - 2][self.y] == EMPTY):
#                print "captured (x - 1 , y)"
                return True

        if self.isOnStrongPosition():

            # x + 1 , y + 1
            if self.board.isOn(self.x + 1,self.y + 1) and self.board.isOn(self.x + 2,self.y + 2) :
                if (self.board.matrix[self.x + 1][self.y + 1] == EMPTY and \
                    self.board.matrix[self.x + 2][self.y + 2] != self.color and \
                    self.board.matrix[self.x + 2][self.y + 2] != EMPTY) \
                    or \
                       (self.board.matrix[self.x + 1][self.y + 1] != self.color and \
                        self.board.matrix[self.x + 1][self.y + 1] != EMPTY and \
                        self.board.matrix[self.x + 2][self.y + 2] == EMPTY):
#                    print "captured (x + 1 , y + 1)"
                    return True

            # x + 1 , y - 1
            if self.board.isOn(self.x + 1,self.y - 1) and self.board.isOn(self.x + 2,self.y - 2) :
                if (self.board.matrix[self.x + 1][self.y - 1] == EMPTY and \
                    self.board.matrix[self.x + 2][self.y - 2] != EMPTY and \
                    self.board.matrix[self.x + 2][self.y - 2] != self.color) \
                    or \
                       (self.board.matrix[self.x + 1][self.y - 1] != self.color and \
                        self.board.matrix[self.x + 1][self.y - 1] != EMPTY and \
                        self.board.matrix[self.x + 2][self.y - 2] == EMPTY):
#                    print "captured (x + 1 , y - 1)"
                    return True

            # x - 1 , y - 1
            if self.board.isOn(self.x - 1,self.y - 1) and self.board.isOn(self.x - 2,self.y - 2) :
                if (self.board.matrix[self.x - 1][self.y - 1] == EMPTY and \
                    self.board.matrix[self.x - 2][self.y - 2] != EMPTY and \
                    self.board.matrix[self.x - 2][self.y - 2] != self.color) \
                    or \
                       (self.board.matrix[self.x - 1][self.y - 1] != self.color and \
                        self.board.matrix[self.x - 1][self.y - 1] != EMPTY and \
                        self.board.matrix[self.x - 2][self.y - 2] == EMPTY):
#                    print "captured (x - 1 , y - 1)"
                    return True

            # x - 1 , y + 1
            if self.board.isOn(self.x - 1,self.y + 1) and self.board.isOn(self.x - 2,self.y + 2) :
                if (self.board.matrix[self.x - 1][self.y + 1] == EMPTY and \
                    self.board.matrix[self.x - 2][self.y + 2] != EMPTY and \
                    self.board.matrix[self.x - 2][self.y + 2] != self.color) \
                    or \
                       (self.board.matrix[self.x - 1][self.y + 1] != self.color and \
                        self.board.matrix[self.x - 1][self.y + 1] != EMPTY and \
                        self.board.matrix[self.x - 2][self.y + 2] == EMPTY):
#                    print "captured (x - 1 , y + 1)"
                    return True

        return False


    def isOnStrongPosition(self):
        if self.x % 2 == self.y % 2 and self.x > 0 and self.x < (self.board.cols - 1) and self.y > 0 and self.y < (self.board.rows - 1) :
            return True
        return False
