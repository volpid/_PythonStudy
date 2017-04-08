#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
import time
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 15
CELLSIZE = 20
assert WINDOW_HEIGHT % CELLSIZE == 0, "Window width must be a multiple of cellsize"
assert WINDOW_HEIGHT % WINDOW_HEIGHT == 0, "Window height must be a multiple of cellsize"
CELL_WIDTH = WINDOW_WIDTH / CELLSIZE
CELL_HEIGHT = WINDOW_HEIGHT / CELLSIZE
BASICFONTSIZE = 18


#RBG
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
DARK_GREY = (40, 40, 40)
BgColor = BLACK

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0

def DoMain() :
    global FPSClock
    global DisplaySurf
    global BasicFont

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Wormy")
    BasicFont = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    ShowStartScreeen()
    while True :
        RunGame()
        ShowGameoverScreen()

def RunGame() :
    startx = random.randint(5, CELL_WIDTH - 6)
    starty = random.randint(5, CELL_HEIGHT - 6)

    wormCoords = [{'x' : startx, 'y' : starty}, 
                  {'x' : startx - 1, 'y' : starty}, 
                  {'x' : startx - 2, 'y' : starty}]

    direction = RIGHT
    apple = GetRandomLocation()

    while True :
        for event in pygame.event.get() :
            if event.type == QUIT :
                Terminate()
            elif event.type == KEYDOWN :
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT :
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT :
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN :
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP :
                    direction = DOWN
                elif event.key == K_ESCAPE :
                    Terminate()

        #Gameover
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELL_WIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELL_HEIGHT :
            return
            
        for wormBody in wormCoords[1:] :
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y'] :
                return

        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y'] :
            apple = GetRandomLocation()
        else :
            del wormCoords[-1]
            
        if direction == UP :
            newHead = {'x' : wormCoords[HEAD]['x'], 'y' : wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN :
            newHead = {'x' : wormCoords[HEAD]['x'], 'y' : wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT :
            newHead = {'x' : wormCoords[HEAD]['x'] - 1, 'y' : wormCoords[HEAD]['y']}
        elif direction == RIGHT :
            newHead = {'x' : wormCoords[HEAD]['x'] + 1, 'y' : wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)

        DisplaySurf.fill(BgColor)
        DrawGrid()
        DrawWorm(wormCoords)
        DrawApple(apple)
        DrawScore(len(wormCoords) - 3)

        pygame.display.update()
        FPSClock.tick(FPS)

def DrawPressKeyMessage() :
    pressKeySurf = BasicFont.render("Press a key to play", True, DARK_GREY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DisplaySurf.blit(pressKeySurf, pressKeyRect)

def CheckForKeyPress() :
    if len(pygame.event.get(QUIT)) > 0 :
        Terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0 :
        return None
    if keyUpEvents[0].key == K_ESCAPE :
        Terminate()

    return keyUpEvents[0].key

def ShowStartScreeen() :
    tileFont = pygame.font.Font("freesansbold.ttf", 100)
    tileSurf1 = tileFont.render("Wormy!", True, WHITE, DARK_GREEN)
    tileSurf2 = tileFont.render("Wormy!", True, GREEN)

    degree1 = 0
    degree2 = 0
    while True :
        DisplaySurf.fill(BgColor)
        rotateSurf1 = pygame.transform.rotate(tileSurf1, degree1)
        rotateRect1 = rotateSurf1.get_rect()
        rotateRect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DisplaySurf.blit(rotateSurf1, rotateRect1)

        rotateSurf2 = pygame.transform.rotate(tileSurf2, degree2)
        rotateRect2 = rotateSurf2.get_rect()
        rotateRect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DisplaySurf.blit(rotateSurf2, rotateRect2)

        DrawPressKeyMessage()

        if CheckForKeyPress() :
            pygame.event.get()
            return
        
        pygame.display.update()
        FPSClock.tick(FPS)
        degree1 += 3
        degree2 += 7

def Terminate() :
    pygame.quit()
    sys.exit()

def GetRandomLocation() :
    return {'x' : random.randint(0, CELL_WIDTH - 1), 'y' : random.randint(0, CELL_HEIGHT - 1)}

def ShowGameoverScreen() :
    gameoverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameoverFont.render("Game", True, WHITE)
    overSurf = gameoverFont.render("Over", True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOW_WIDTH / 2, 10)
    overRect.midtop = (WINDOW_WIDTH / 2, gameRect.height + 10 + 25)

    DisplaySurf.blit(gameSurf, gameRect)
    DisplaySurf.blit(overSurf, overRect)
    DrawPressKeyMessage()
    
    pygame.display.update()
    pygame.time.wait(500)
    CheckForKeyPress()

    while True :
        if CheckForKeyPress() :
            pygame.event.get()
            return 

def DrawScore(score) :
    scoreSurf = BasicFont.render("Score %s" % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
    DisplaySurf.blit(scoreSurf, scoreRect)

def DrawWorm(wormCoors) :
    for coord in wormCoors :
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DisplaySurf, DARK_GREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DisplaySurf, GREEN, wormInnerSegmentRect)

def DrawApple(coord) :
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DisplaySurf, RED, appleRect)

def DrawGrid():
    for x in range(0, WINDOW_WIDTH, CELLSIZE) :
        pygame.draw.line(DisplaySurf, DARK_GREY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELLSIZE) :
        pygame.draw.line(DisplaySurf, DARK_GREY, (0, y), (WINDOW_WIDTH, y))

if __name__ == "__main__" :
    DoMain()
