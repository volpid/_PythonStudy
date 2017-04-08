#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
import time
from pygame import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, "board needs even number"

XMARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
YMARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

#preDefined Color RGB
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (255, 0, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"

AllColors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
AllShapes = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(AllColors) * len(AllShapes) * 2 >= BOARD_HEIGHT * BOARD_HEIGHT, "board is too big for the number of shapes/color defined"

def DoMain() :
    global FPSClock
    global DisplaySurf

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Memory Game")

    mainBoard = GetRandomizedBoard()
    revealBoxes = GernerateRevealBoxesData(False)

    firstSelection = None

    DisplaySurf.fill(BGCOLOR)
    StartGameAnimation(mainBoard)

    while True :
        mouseClicked = False

        DisplaySurf.fill(BGCOLOR)
        DrawBoard(mainBoard, revealBoxes)

        for event in pygame.event.get() :
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION :
                (mousex, mousey) = event.pos
            elif event.type == MOUSEBUTTONUP :
                (mousex, mousey) = event.pos
                mouseClicked = True

        (boxx, boxy) = GetBoxAtPixel(mousex, mousey)
        if (boxx != None) and (boxy != None) :
            if not revealBoxes[boxx][boxy] :
                DrawHighlightBox(boxx, boxy)
            if (not revealBoxes[boxx][boxy]) and (mouseClicked == True) :
                RevealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealBoxes[boxx][boxy] = True
                
                if firstSelection == None :
                    firstSelection = (boxx, boxy)
                else :
                    (iconShape1, iconColor1) = GetShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    (iconShape2, iconColor2) = GetShapeAndColor(mainBoard, boxx, boxy)

                    if (iconShape1 != iconShape2) or (iconColor1 != iconColor2) :
                        pygame.time.wait(1000)
                        CoverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealBoxes[boxx][boxy] = False

                    elif HasWon(revealBoxes) :
                        GameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = GetRandomizedBoard()
                        revealBoxes = GernerateRevealBoxesData(False)

                        DrawBoard(mainBoard, revealBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        StartGameAnimation(mainBoard)

                    firstSelection = None

        pygame.display.update()
        FPSClock.tick(FPS)

def GernerateRevealBoxesData(val) :
    revealBoxes = []
    for i in range(BOARD_WIDTH) :
        revealBoxes.append([val] * BOARD_HEIGHT)

    return revealBoxes

def GetRandomizedBoard() :
    icons = []
    for color in AllColors :
        for shape in AllShapes :
            icons.append((shape, color))

    random.shuffle(icons)
    numIconUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:numIconUsed] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARD_WIDTH) :
        column = []
        for y in range(BOARD_HEIGHT) :
            column.append(icons[0])
            del icons[0]
        board.append(column)

    return board

def SplitIntoGroupsOf(groupSize, theList) :
    result = []
    for i in range(0, len(theList), groupSize) :
        result.append(theList[i : i + groupSize])
    return result

def LeftTopCoordOfBox(boxx, boxy) :
    left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE) + YMARGIN

    return (left, top)

def GetBoxAtPixel(x, y) :
    for boxx in range(BOARD_WIDTH) :
        for boxy in range(BOARD_HEIGHT) :
            (left, top) = LeftTopCoordOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)

            if boxRect.collidepoint(x, y) : 
                return (boxx, boxy)
    return (None, None)

def DrawIcon(shape, color, boxx, boxy) :
    quater = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.5)

    (left, top) = LeftTopCoordOfBox(boxx, boxy)
    if shape == DONUT :
        pygame.draw.circle(DisplaySurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DisplaySurf, BGCOLOR, (left + half, top + half), quater - 5)
    elif shape == SQUARE :
        pygame.draw.rect(DisplaySurf, color, (left + quater, top + quater, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND :
        pygame.draw.polygon(DisplaySurf, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES :
        for i in range(0, BOX_SIZE, 4) :
            pygame.draw.line(DisplaySurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(DisplaySurf, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL :
        pygame.draw.ellipse(DisplaySurf, color, (left, top + quater, BOX_SIZE, half))

def GetShapeAndColor(board, boxx, boxy) :
    return (board[boxx][boxy][0], board[boxx][boxy][1])

def DrawBoxCovers(board, boxes, coverage) :
    for box in boxes :
        (left, top) = LeftTopCoordOfBox(box[0], box[1])
        pygame.draw.rect(DisplaySurf, BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
        (shape, color) = GetShapeAndColor(board, box[0], box[1])
        DrawIcon(shape, color, box[0], box[1])
        if coverage > 0 :
            pygame.draw.rect(DisplaySurf, BOXCOLOR, (left, top, coverage, BOX_SIZE))
    pygame.display.update()
    FPSClock.tick(FPS)

def RevealBoxesAnimation(board, boxesToReveal) :
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED) :
        DrawBoxCovers(board, boxesToReveal, coverage)

def CoverBoxesAnimation(board, boxesToCover) :
    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED) :
        DrawBoxCovers(board, boxesToCover, coverage)

def DrawBoard(board, revealed) :
    for boxx in range(BOARD_WIDTH) :
        for boxy in range(BOARD_HEIGHT) :
            (left, top) = LeftTopCoordOfBox(boxx, boxy)
            if not revealed[boxx][boxy] :
                pygame.draw.rect(DisplaySurf, BOXCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else :
                (shape, color) = GetShapeAndColor(board, boxx, boxy)
                DrawIcon(shape, color, boxx, boxy)

def DrawHighlightBox(boxx, boxy) :
    (left, top) = LeftTopCoordOfBox(boxx, boxy)
    pygame.draw.rect(DisplaySurf, HIGHLIGHTCOLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)

def StartGameAnimation(board) :
    coveredBoxes = GernerateRevealBoxesData(False)
    boxes = []

    for x in range(BOARD_WIDTH) :
        for y in range(BOARD_HEIGHT) :
            boxes.append((x, y))

    random.shuffle(boxes)
    boxGroups = SplitIntoGroupsOf(8, boxes)

    DrawBoard(board, coveredBoxes)
    for boxGroup in boxGroups :
        RevealBoxesAnimation(board, boxGroup)
        CoverBoxesAnimation(board, boxGroup)

    #boxes = []
    #for x in range(BOARD_WIDTH) :
    #    for y in range(BOARD_HEIGHT) :
    #        boxes.append((x, y))
    #RevealBoxesAnimation(board, boxes)    
    #pygame.time.wait(1000)
    #CoverBoxesAnimation(board, boxes)

def GameWonAnimation(board) :
    coveredBoxes = GernerateRevealBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13) :
        (color1, color2) = (color2, color1)
        DisplaySurf.fill(color1)
        DrawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def HasWon(revealedBoxes) :
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == "__main__" :
    DoMain()
