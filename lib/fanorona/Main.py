# -*- coding: utf-8 -*-

__author__ = 'Thierry Randrianiriana <randrianiriana@gmail.com>'
__license__ = 'GNU General Public License version 2 or later'
__copyright__ = 'Copyright (C) 2007-2011 Thierry Randrianiriana'

import sys
from const import *
import pygame
import random
from pygame.locals import *
from Board import Board
from Stone import Stone
from Player import Player
from Utils import utils
from menu import cMenu, EVENT_CHANGE_STATE

import gettext
gettext.bindtextdomain(DOMAIN,LOCALEDIR)
gettext.textdomain(DOMAIN)
_ = gettext.gettext

class Main :
    def __init__(self,player):
        WINX = 500
        WINY = 300
              
        pygame.init()
        self.screen = pygame.display.set_mode((WINX, WINY))

        background = utils.load_image(BOARD_BACKGROUND)
        self.screen.blit(background, (0, 0))

        self.player = player
        pygame.display.set_caption('Fanorona')
        icon = utils.load_icon(ICON_32)
        pygame.display.set_icon(icon)
        
    def run(self,timeout):
        TIMEOUT = timeout

        board = Board()
        board.populate()

        status_black = utils.load_image(STATUS_BLACK)
        status_white = utils.load_image(STATUS_WHITE)
        status_red = utils.load_image(STATUS_RED)
        status_disabled = utils.load_image(STATUS_DISABLED)
        cmd_exit = utils.load_image(EXIT)
        cmd_stop = utils.load_image(PLAYER_STOP)
        cmd_play = utils.load_image(PLAYER_PLAY)
        cmd_pause = utils.load_image(PLAYER_PAUSE)
        cmd_pass = utils.load_image(PLAYER_END)
        background = utils.load_image(BOARD_BACKGROUND)

        background.blit(cmd_exit,(0,0))
        background.blit(cmd_stop,(22,0))
        background.blit(cmd_pause,(44,0))
        background.blit(cmd_play,(66,0))
        background.blit(cmd_pass,(88,0))

        rand = random.randint(0,1000)
        selected = BLACK

        if rand % 2 == 0 :
            selected = RED

        rand = random.randint(0,1000)
        ai_color = RED

        if rand % 2 == 0 :
            ai_color = BLACK

        timeout = TIMEOUT
        time_left = TIMEOUT
        white = False
        winner = None
        status = 'stop'

        #menu
        menu = cMenu(5, 5, 2, 5, 'vertical', 100, self.screen,
               [( _('New Game'),  1, None), 
                ( _('One Player'),  2, None),
                ( _('Two Players'), 3, None),
                ( _('Return'),      4, None),
                ( _('Exit'),        5, None)])
        menu.set_center(True, True)
        menu.set_alignment('center', 'center')
        show_menu = True
        state = 0
        prev_state = 1
        rect_list = []

        while 1:
            if show_menu:
                # Check if the state has changed, if it has, then post a user event to
                # the queue to force the menu to be shown at least once
                if prev_state != state:
                    pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                    prev_state = state

                # Get the next event
                e = pygame.event.wait()

                # Update the menu, based on which "state" we are in - When using the menu
                # in a more complex program, definitely make the states global variables
                # so that you can refer to them by a name
                if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                    if state == 0:
                        rect_list, state = menu.update(e, state)
                    elif state == 1:
                        print 'New Game'
                        state = 0
                        board = Board()
                        board.populate()
                        status = 'play'
                        show_menu = False
                    elif state == 2:
                        print 'One Player'
                        state = 0
                        self.player = 1
                        show_menu = False
                    elif state == 3:
                        print 'Two Players'
                        self.player = 2
                        show_menu = False
                        state = 0
                    elif state == 4:
                        print 'Return'
                        show_menu = False
                        state = 0
                    else:
                        print 'Exit!'
                        pygame.quit()
                        sys.exit()

                # Quit if the user presses the exit button
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Update the screen
                pygame.display.update(rect_list)
                
                if show_menu: 
                    continue
            
            #AI
            if self.player == 1 and ai_color == selected and status == 'play':
                p = Player(board , ai_color)
                p.play(self.screen)
                selected = utils.invert_color(selected)
                timeout = TIMEOUT
                board.unselectedAll()

            for event in pygame.event.get():
                x = y = -1
                if event.type == QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    show_menu = True
                elif event.type == MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()

                    (x , y, pass_round) = board.getSelectedPosition(m_pos)

                    if pass_round:
                        selected = utils.invert_color(selected)
                        board.unselectedAll()
                        continue

                    if x >= 0 and y >= 0 :

                        if board.stoneExists(x,y) :
                            status = 'play'

                            oStone = Stone(board,x,y)
                            if oStone.color == selected and oStone.canMove() :
                                sStone = Stone(board,x,y)
                                sStone.selected()

                            else :
                                try:
                                    if oStone.mustChoose():
                                        timeout = TIMEOUT
                                        sStone.choose(x,y)
                                        if sStone.canMove():
                                            sStone.selected()

                                        else:
                                            selected = utils.invert_color(sStone.color)
                                            board.unselectedAll()

                                except:
                                    print "object sStone doesn't exist"

                        else:
                            (old_x,old_y,color) = board.getSelectedStone()
                            if old_x>=0 and old_y>=0 and color>0 :
                                if sStone.move(x,y) :
                                    timeout = TIMEOUT
                                    if sStone.mustChoose():
                                        sStone.selected()

                                    elif sStone.canMove() :
                                        sStone.selected()


                                    else:
                                        selected = utils.invert_color(sStone.color)
                                        sStone.unselected()
                    #action
                    else:
                        (m_x , m_y) = m_pos
                        if m_x < 22 and m_y < 22:
                            # quit
                            return
                        elif m_x > 22 and m_x < 44 and m_y < 22:
                            # stop
                            board = Board()
                            board.populate()
                            # print "stop"
                            status = 'stop'

                        elif m_x > 44 and m_x < 66 and m_y < 22:
                            # pause
                            # print "pause"
                            if status == 'pause':
                                status = 'play'
                                timeout = time_left
                                time_left = 0

                            else:
                                status = 'pause'
                                time_left = timeout

                        elif m_x > 66 and m_x < 88 and m_y < 22:
                            # play
                            # print "play"
                            if status == 'pause':
                                timeout = time_left
                                time_left = 0

                            status = 'play'
                            if winner != None:
                                board = Board()
                                board.populate()

                        elif m_x > 88 and m_x < 110 and m_y < 22:
                            # play
                            # print "pass"
                            selected=utils.invert_color(selected)
                            timeout=TIMEOUT
                            status = 'play'

            self.screen.blit(background, (0, 0))

            #check if a player wins
            winner = board.checkWinner();
            if winner != None:
                font = pygame.font.Font(pygame.font.get_default_font(), 26)
                text =  _('%s wins') % utils.getColorName(winner)
                text = font.render(text, 1, (10, 10, 10))
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx
                self.screen.blit(text, textpos)
                status = 'pause'

            #show timer
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            if status == 'play':
                text =  _('%d seconds left') % (timeout/1000)
                text = font.render(text, 1, (10, 10, 10))
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx
                self.screen.blit(text, textpos)
            elif status == 'pause' and winner == None :
                text =  _('%d seconds left') % (time_left/1000)
                text = font.render(text, 1, (10, 10, 10))
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx
                self.screen.blit(text, textpos)

            #blink
            if status == 'play':
                if timeout < 10000 and not white:
                    if selected == BLACK :
                        self.screen.blit(status_white, (500-40, 0))
                        self.screen.blit(status_disabled, (500-20, 0))
                    else:
                        self.screen.blit(status_disabled, (500-40, 0))
                        self.screen.blit(status_white, (500-20, 0))
                    white = True

                else :
                    if selected == BLACK :
                        self.screen.blit(status_black, (500-40, 0))
                        self.screen.blit(status_disabled, (500-20, 0))
                    else:
                        self.screen.blit(status_disabled, (500-40, 0))
                        self.screen.blit(status_red, (500-20, 0))
                    white = False

            #show
            board.populate_gui(self.screen)
            pygame.display.update()
            pygame.time.delay(DELAY)

            #time out
            timeout -= DELAY
            if status == "stop" or status =="pause":
                timeout = TIMEOUT

            if timeout < 0 :
                selected = utils.invert_color(selected)
                board.unselectedAll()
                timeout = TIMEOUT
