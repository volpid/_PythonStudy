#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
import time
from pygame.locals import *
#from pygame import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 25
BOXSIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = '.'

MOVE_SIDEWAYS_FREQ = 0.15
MOVE_DOWN_FREQ = 0.1

XMARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * BOXSIZE) /2)
TOPMARGIN = int(WINDOW_HEIGHT - (BOARD_HEIGHT * BOXSIZE) - 5)

#RGB
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
RED = (155, 0, 0)
LIGHT_RED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHT_GREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHT_BLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHT_YELLOW = (175, 175, 20)
BLACK = (0, 0, 0)

BorderColor = BLUE
BgColror = BLACK
TextColor = WHITE
TextShadowColor = GRAY
Colors = (BLUE, GREEN, RED, YELLOW)
LightColors = (LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED, LIGHT_YELLOW)
assert len(Colors) == len(LightColors)

TemplateWidth = 5
TemplateHeight = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '...O.',
                     '..OO.',
                     '..O..',
                     '.....']]

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '..O..'],
                    ['.....',
                     '.....',
                     'OOOOO',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',                     
                     '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '...O.',
                      '.....'],
                      ['.....',
                       '..OO.',
                       '..O..',
                       '..O..',
                       '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',                     
                     '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '.O...',
                      '.....'],
                      ['.....',
                       '..O..',
                       '..O..',
                       '..OO.',
                       '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',                     
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',                     
                     '.....'],
                     ['.....',
                      '.....',
                      '.OOO.',
                      '..O..',
                      '.....'],
                      ['.....',
                       '..O..',
                       '..OO.',
                       '..O..',
                       '.....']]

Shapes = {'S' : S_SHAPE_TEMPLATE, 
          'Z' : Z_SHAPE_TEMPLATE, 
          'J' : J_SHAPE_TEMPLATE, 
          'L' : L_SHAPE_TEMPLATE, 
          'I' : I_SHAPE_TEMPLATE, 
          'O' : O_SHAPE_TEMPLATE, 
          'T' : T_SHAPE_TEMPLATE}

def DoMain() :
    global FPSClock
    global DisplaySurf
    global BasicFont
    global BigFont

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetromino")

    BasicFont = pygame.font.Font("freesansbold.ttf", 18)
    BigFont = pygame.font.Font("freesansbold.ttf", 100)

    ShowTextScreen('Tetromno')
    while True :
        if random.randint(0, 1) == 0 :
            pygame.mixer.music.load('./_Resource/tetrisb.mid')
        else :
            pygame.mixer.music.load('./_Resource/tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        
        RunGame()
        pygame.mixer.music.stop()
        ShowTextScreen('GameOver')

def RunGame() :
    board = GetBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft= False
    movingRight = False
    score = 0

    (level, fallFreq) = CalculateLevelAndFreq(score)
    
    fallingPiece = GetNewPiece()
    nextPiece = GetNewPiece()

    while True :
        if fallingPiece == None :
            fallingPiece = nextPiece
            nextPiece = GetNewPiece()
            lastFallTime = time.time()

            if not IsValidPosition(board, fallingPiece) :
                return

        CheckForQuit()
        for event in pygame.event.get() :
            if event.type == KEYUP :
                if event.key == K_p :
                    DisplaySurf.fill(BgColror)
                    pygame.mixer.music.stop()
                    ShowTextScreen("Paused")
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_LEFT or event.key == K_a :
                    movingLeft = False
                elif event.key == K_RIGHT or event.key == K_d :
                    movingRight = False
                elif event.key == K_LEFT or event.key == K_a :
                    movingDown = False
            elif event.type == KEYDOWN :
                if (event.key == K_LEFT or event.key == K_a) and IsValidPosition(board, fallingPiece, adjX = -1) :
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT or event.key == K_d) and IsValidPosition(board, fallingPiece, adjX = 1) :
                    fallingPiece['x'] += 1
                    movingLeft = False
                    movingRight = True
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_UP or event.key == K_w) :
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(Shapes[fallingPiece['shape']])
                    if not IsValidPosition(board, fallingPiece) :
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(Shapes[fallingPiece['shape']])
                elif (event.key == K_q) :
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(Shapes[fallingPiece['shape']])
                    if not IsValidPosition(board, fallingPiece) :
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(Shapes[fallingPiece['shape']])
                elif (event.key == K_DOWN or event.key == K_s) :
                    movingDown == True
                    if IsValidPosition(board, fallingPiece, adjY = 1) :
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                elif (event.key == K_SPACE) :
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARD_HEIGHT) :
                        if not IsValidPosition(board, fallingPiece, adjY = i) :
                            break
                        fallingPiece['y'] += i - 1

        if movingDown and time.time() - lastMoveDownTime > MOVE_DOWN_FREQ and IsValidPosition(board, fallingPiece, adjY = 1) :
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        if time.time() - lastFallTime > fallFreq :
            if not IsValidPosition(board, fallingPiece, adjY = 1) :
                AddToBoard(board, fallingPiece)
                score += RemoveCompleteLines(board)
                (level, fallFreq) = CalculateLevelAndFreq(score)
                fallingPiece = None;
            else :
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        DisplaySurf.fill(BgColror)
        DrawBoard(board)
        DrawStatus(score, level)
        DrawNextPiece(nextPiece)

        if fallingPiece != None :
            DrawPiece(fallingPiece)

        pygame.display.update()
        FPSClock.tick(FPS)

def MakeTextObjs(text, font, color) :
    surf = font.render(text, True, color)
    return (surf, surf.get_rect())

def Terminate() :
    pygame.quit()
    sys.exit()

def CheckForQuit() :
    for event in pygame.event.get(QUIT) :
        Terminate()
    for event in pygame.event.get(KEYUP) :
        if event.key == K_ESCAPE :
            Terminate()
        pygame.event.post(event)

def CheckForKeyPresss() :
    CheckForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]) :
        if event.type == KEYDOWN :
            continue
        return event.key
    return None

def ShowTextScreen(text) :
    (titleSurf, titleRect) = MakeTextObjs(text, BigFont, TextShadowColor)
    titleRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DisplaySurf.blit(titleSurf, titleRect)

    (titleSurf, titleRect) = MakeTextObjs(text, BigFont, TextColor)
    titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    DisplaySurf.blit(titleSurf, titleRect)

    (pressKyeSurf, pressKeyRect) = MakeTextObjs("Press a key to play", BasicFont, TextColor)
    pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    DisplaySurf.blit(pressKyeSurf, pressKeyRect)

    while CheckForKeyPresss() == None :
        pygame.display.update()
        FPSClock.tick()

def CalculateLevelAndFreq(score) :
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return (level, fallFreq)

def GetNewPiece() :
    shape = random.choice(list(Shapes.keys()))
    newPiece = {'shape' : shape,
                'rotation' : random.randint(0, len(Shapes[shape]) - 1),
                'x' : int(BOARD_WIDTH / 2) - int(TemplateWidth / 2),
                'y' : -2,
                'color' : random.randint(0, len(Colors) - 1)}
    return newPiece

def AddToBoard(board, piece) :
    for x in range(TemplateWidth) :
        for y in range(TemplateHeight) :
            if Shapes[piece['shape']][piece['rotation']][y][x] != BLANK :
                board[x + piece['x']][y + piece['y']] = piece['color']

def GetBlankBoard() :
    board = []
    for i in range(BOARD_WIDTH) :
        board.append([BLANK] * BOARD_HEIGHT)

    return board

def IsOnBoard(x, y) :
    return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT

def IsValidPosition(board, piece, adjX = 0, adjY = 0) :
    for x in range(TemplateWidth) :
        for y in range(TemplateHeight) :
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or Shapes[piece['shape']][piece['rotation']][y][x] == BLANK :
                continue
            if not IsOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY) :
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK :
                return False
    return True

def IsCompleteLine(board, y) :
    for x in range(BOARD_WIDTH) :
        if board[x][y] == BLANK :
            return False
    return True

def RemoveCompleteLines(board) :
    numLinesRemoved = 0
    y = BOARD_HEIGHT - 1
    while y >= 0 :
        if IsCompleteLine(board, y):
            for pullDownY in range(y, 0, -1) :
                for x in range(BOARD_WIDTH) :
                    board[x][pullDownY] = board[x][pullDownY - 1]
            for x in range(BOARD_WIDTH) :
                board[x][0] = BLANK
            numLinesRemoved += 1
        else :
            y -= 1
    return numLinesRemoved

def ConvertToPixelCoords(boxx, boxy) :
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def DrawBox(boxx, boxy, color, pixelx = None, pixely = None) :
    if color == BLANK :
        return
    if pixelx == None and pixely == None :
        (pixelx, pixely) = ConvertToPixelCoords(boxx, boxy)

    pygame.draw.rect(DisplaySurf, Colors[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DisplaySurf, LightColors[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def DrawBoard(board) :
    pygame.draw.rect(DisplaySurf, BorderColor, (XMARGIN - 3, TOPMARGIN - 7, (BOARD_WIDTH * BOXSIZE) + 8, (BOARD_HEIGHT * BOXSIZE) + 8), 5)
    pygame.draw.rect(DisplaySurf, BgColror, (XMARGIN, TOPMARGIN, BOXSIZE * BOARD_WIDTH, BOXSIZE * BOARD_HEIGHT))

    for x in range(BOARD_WIDTH) :
        for y in range(BOARD_HEIGHT) :
            DrawBox(x, y, board[x][y])

def DrawStatus(score, level) :
    scoreSurf = BasicFont.render("Score %s" % score, True, TextColor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 150, 20)
    DisplaySurf.blit(scoreSurf, scoreRect)

    levelSurf = BasicFont.render('Level %s' % level, True, TextColor)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_WIDTH - 150, 50)
    DisplaySurf.blit(levelSurf, levelRect)

def DrawPiece(piece, pixelx = None, pixely = None) :
    shapeToDraw = Shapes[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None :
        (pixelx, pixely) = ConvertToPixelCoords(piece['x'], piece['y'])

    for x in range(TemplateWidth) :
        for y in range(TemplateWidth) :
            if shapeToDraw[y][x] != BLANK :
                DrawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def DrawNextPiece(piece) :
    nextSurf = BasicFont.render('Next', True, TextColor)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOW_WIDTH - 120, 80)
    DisplaySurf.blit(nextSurf, nextRect) 
    DrawPiece(piece, pixelx = WINDOW_WIDTH - 120, pixely = 100)

if __name__ == "__main__" :
    DoMain()
