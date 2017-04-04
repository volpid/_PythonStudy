#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
from pygame import *

BOARD_WIDTH = 4
BOARD_HEIGHT = 4
TILE_SIZE = 80
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVYBLUE = (60, 60, 100)
DARKTURQUISE = (3, 54, 74)
GREEN = (0, 255, 0)

BGCOLOR = DARKTURQUISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BOARDERCOLOR = NAVYBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
YMARGIN = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

def DoMain() :
    global FPSClock
    global DisplaySurf
    global BasicFont
    global ResetSurf
    global ResetRect
    global NewSurf
    global NewRect
    global SolveSurf
    global SolveRect

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Slide Puzzle")
    BasicFont = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    (ResetSurf, ResetRect) = MakeText("Reset", TEXTCOLOR, TILECOLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 90)
    (NewSurf, NewRect) = MakeText("New Game", TEXTCOLOR, TILECOLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60)
    (SolveSurf, SolveRect) = MakeText("Solve", TEXTCOLOR, TILECOLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)

    (mainBoard, solutionBoard) = GenerateNewPuzzle(80)
    SOLVEDBOARD = GetStartingBoard()

    allMoves = []

    while True :
        slideTo = None
        msg =""

        if mainBoard == SOLVEDBOARD :
            msg = "solved"
        DrawBoard(mainBoard, msg)

        CheckForQuit()
        for event in pygame.event.get() :
            if event.type == MOUSEBUTTONUP :
                (spotx, spoty) = GetSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None) :
                    if ResetRect.collidepoint(event.pos) :
                        ResetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NewRect.collidepoint(event.pos) :
                        (mainBoard, solutionBoard) = GenerateNewPuzzle(80)
                        allMoves = []
                    elif SolveRect.collidepoint(event.pos) :
                        ResetAnimation(mainBoard, solutionBoard + allMoves)
                        allMoves = []
                else :
                    (blankx, blanky) = GetBlankPosition(mainBoard)
                    if (spotx == blankx + 1) and (spoty == blanky) :
                        slideTo = LEFT
                    elif (spotx == blankx - 1) and (spoty == blanky) :
                        slideTo = RIGHT
                    elif (spotx == blankx) and (spoty == blanky + 1) :
                        slideTo = UP
                    elif (spotx == blankx) and (spoty == blanky - 1) :
                        slideTo = DOWN

            elif event.type == KEYUP :
                if event.key in (K_LEFT, K_a) and IsValidMove(mainBoard, LEFT) :
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and IsValidMove(mainBoard, RIGHT) :
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and IsValidMove(mainBoard, UP) :
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and IsValidMove(mainBoard, DOWN) :
                    slideTo = DOWN

        if slideTo :
            SlideAnimation(mainBoard, slideTo, "click tile or press arrow to slide", 8)
            MakeMove(mainBoard, slideTo)
            allMoves.append(slideTo)

        pygame.display.update()
        FPSClock.tick(FPS)

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

def GetStartingBoard() :
    counter = 1
    board = []
    for x in range(BOARD_WIDTH) :
        column = []
        for y in range(BOARD_HEIGHT) :
            column.append(counter)
            counter += BOARD_WIDTH
        board.append(column)
        counter -= BOARD_WIDTH * (BOARD_HEIGHT - 1) +BOARD_WIDTH - 1

    board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = None
    return board

def GetBlankPosition(board) :
    for x in range(BOARD_WIDTH) :
        for y in range(BOARD_HEIGHT) :
            if board[x][y] == None : 
                return (x, y)

def MakeMove(board, move) :
    (blankx, blanky) = GetBlankPosition(board)

    if move == UP :
        (board[blankx][blanky], board[blankx][blanky + 1]) = (board[blankx][blanky + 1], board[blankx][blanky])
    elif move == DOWN :
        (board[blankx][blanky], board[blankx][blanky - 1]) = (board[blankx][blanky - 1], board[blankx][blanky])
    elif move == LEFT :
        (board[blankx][blanky], board[blankx + 1][blanky]) = (board[blankx + 1][blanky], board[blankx][blanky])
    elif move == RIGHT :
        (board[blankx][blanky], board[blankx - 1][blanky]) = (board[blankx - 1][blanky], board[blankx][blanky])


def IsValidMove(board, move) :
    (blankx, blanky) = GetBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) \
        or (move == DOWN and blanky != 0) \
        or (move == LEFT and blankx != len(board) - 1) \
        or (move == RIGHT and blankx != 0)

def GetRandomMove(board, lastMove) :
    validMove = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not IsValidMove(board, DOWN) :
        validMove.remove(DOWN)
    if lastMove == DOWN or not IsValidMove(board, UP) :
        validMove.remove(UP)
    if lastMove == LEFT or not IsValidMove(board, RIGHT) :
        validMove.remove(RIGHT)
    if lastMove == RIGHT or not IsValidMove(board, LEFT) :
        validMove.remove(LEFT)

    return random.choice(validMove)

def GetLeftTopOfTile(tilex, tiley) :
    left = XMARGIN + (tilex * TILE_SIZE) + (tilex - 1)
    top = YMARGIN + (tiley * TILE_SIZE) + (tiley - 1)

    return (left, top)

def GetSpotClicked(board, x, y) :
    for tilex in range(len(board)) :
        for tiley in range(len(board[0])) :
            (left, top) = GetLeftTopOfTile(tilex, tiley)
            tileRect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tileRect.collidepoint(x, y) :
                return (tilex, tiley)
    return (None, None)

def DrawTile(tilex, tiley, number, adjx = 0, adjy = 0) :
    (left, top) = GetLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DisplaySurf, TILECOLOR, (left + adjx, top + adjy, TILE_SIZE, TILE_SIZE))
    textSurf = BasicFont.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = (left + int(TILE_SIZE / 2) + adjx, top + int(TILE_SIZE / 2) + adjy)
    DisplaySurf.blit(textSurf, textRect)

def MakeText(text, color, bgcolor, top, left) :
    textSurf = BasicFont.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)

    return (textSurf, textRect)

def DrawBoard(board, message) :
    DisplaySurf.fill(BGCOLOR)
    if message :
        (textSurf, textRect) = MakeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DisplaySurf.blit(textSurf, textRect)

    for tilex in range(len(board)) :
        for tiley in range(len(board[0])) :
            if board[tilex][tiley] :
                DrawTile(tilex, tiley, board[tilex][tiley])

    (left, top) = GetLeftTopOfTile(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE
    pygame.draw.rect(DisplaySurf, BOARDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DisplaySurf.blit(ResetSurf, ResetRect)
    DisplaySurf.blit(NewSurf, NewRect)
    DisplaySurf.blit(SolveSurf, SolveRect)

def SlideAnimation(board, direction, message, animationSpeed) :
    (blankx, blanky) = GetBlankPosition(board)

    if direction == UP :
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN :
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT :
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT :
        movex = blankx - 1
        movey = blanky

    DrawBoard(board, message)
    baseSurf = DisplaySurf.copy()
    (moveLeft, moveTop) = GetLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILE_SIZE, TILE_SIZE))

    for i in range(0, TILE_SIZE, animationSpeed) :
        CheckForQuit()
        DisplaySurf.blit(baseSurf, (0, 0))
        if direction == UP :
            DrawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN :
            DrawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT :
            DrawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT :
            DrawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSClock.tick(FPS)

def GenerateNewPuzzle(numSlides) :
    sequence = []
    board = GetStartingBoard()
    DrawBoard(board, "")
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides) :
        move = GetRandomMove(board, lastMove)
        SlideAnimation(board, move, "Generate new puzzle...", int(TILE_SIZE / 3))
        MakeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

def ResetAnimation(board, allMoves) :
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves :
        if move == UP :
            oppositeMove = DOWN
        elif move == DOWN :
            oppositeMove = UP
        elif move == LEFT :
            oppositeMove = RIGHT
        elif move == RIGHT :
            oppositeMove = LEFT
        SlideAnimation(board, oppositeMove, "", int(TILE_SIZE / 2))
        MakeMove(board, oppositeMove)

if __name__ == "__main__" :
    DoMain()
