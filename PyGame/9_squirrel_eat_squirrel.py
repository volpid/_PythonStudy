#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
import time
import math
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_WIDTH_HALF = int(WINDOW_WIDTH / 2)
WINDOW_HEIGHT_HALF = int(WINDOW_HEIGHT / 2)
BASICFONTSIZE = 32

GRASS_COLOR = (24, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERA_SLACK = 90
MOVERATE = 9
BOUNCERATE = 6
BOUNCEHEIGHT = 30
STARTSIZE = 25
WINSIZE = 300
INVULNTIME = 2
GAMEOVERTIME = 4
MAXHEALTH = 3

NUMGRASS = 80
NUMSQUIRRES = 30
SQUIRRELMINSPEED = 3
SQUIRRELMAXSPEED = 7
DIRCHANGEFREQ = 2

LEFT = 'left'
RIGHT = 'right'

def DoMain() :
    global FPSClock
    global DisplaySurf
    global BasicFont
    global L_SQUIR_IMG
    global R_SQUIR_IMG
    global GRASS_IMGS

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Squirrel Eat Squirrel")
    BasicFont = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    L_SQUIR_IMG = pygame.image.load('./_Resource/squirrel.png')
    R_SQUIR_IMG = pygame.transform.flip(L_SQUIR_IMG, True, False)
    GRASS_IMGS = []

    for i in range(1, 5) :
        GRASS_IMGS.append(pygame.image.load('./_Resource/grass%s.png' % i))

    while True :
        RunGame()

def RunGame() :
    invulneralMode = False
    invulneralStartTime = 0
    gameOverMode = False
    gameOverStartTime = 0
    winMode = False

    gameOverSurf = BasicFont.render("GameOver", True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF)

    winSurf = BasicFont.render("You have achieved OMEGA SQUIRREL", True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF)

    winSurf2 = BasicFont.render("Press \"r\" to restart.", True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF + 30)

    camerax = 0
    cameray = 0

    grassObjs = []
    squirrelObjs = []

    playerObj = {"surface" : pygame.transform.scale(L_SQUIR_IMG, (STARTSIZE, STARTSIZE)),
                 "facing" : LEFT,
                 "size" : STARTSIZE,
                 "x" : WINDOW_WIDTH_HALF,
                 "y" : WINDOW_HEIGHT_HALF,
                 "bounce" : 0,
                 "health" : MAXHEALTH}

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    for i in range(10) :
        grassObjs.append(MakeNewGrass(camerax, cameray))
        grassObjs[i]['x'] = random.randint(0, WINDOW_WIDTH)
        grassObjs[i]['y'] = random.randint(0, WINDOW_HEIGHT)

    while True :
        if invulneralMode and time.time() - invulneralStartTime > INVULNTIME :
            invulneralMode = False

        for sObj in squirrelObjs :
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']
            sObj['bounce'] += 1
            if sObj['bounce'] > sObj['bouncerate'] :
                sObj['bounce'] = 0

            if random.randint(0, 99) < DIRCHANGEFREQ :
                sObj['movex'] = GetRandomVelocity()
                sObj['movey'] = GetRandomVelocity()
                if sObj['movex'] > 0 :
                    sObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sObj['width'], sObj['height']))
                else :
                    sObj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (sObj['width'], sObj['height']))

            
        for i in range(len(grassObjs) - 1, -1, -1) :
            if IsOutsideActiveArea(camerax, cameray, grassObjs[i]) :
                del grassObjs[i]

        for i in range(len(squirrelObjs) - 1, -1, -1) :
            if IsOutsideActiveArea(camerax, cameray, squirrelObjs[i]) :
                del squirrelObjs[i]

        while len(grassObjs) < NUMGRASS :
            grassObjs.append(MakeNewGrass(camerax, cameray))

        while len(squirrelObjs) < NUMSQUIRRES :
            squirrelObjs.append(MakeNewSquirrel(camerax, cameray))

        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        if (camerax + WINDOW_WIDTH_HALF) - playerCenterx > CAMERA_SLACK :
            camerax = playerCenterx + CAMERA_SLACK - WINDOW_WIDTH_HALF
        elif playerCenterx - (CAMERA_SLACK + WINDOW_WIDTH_HALF) > CAMERA_SLACK :
            camerax = playerCenterx - CAMERA_SLACK - WINDOW_WIDTH_HALF
        elif (cameray + WINDOW_HEIGHT_HALF) - playerCentery > CAMERA_SLACK :
            cameray = playerCentery + CAMERA_SLACK - WINDOW_HEIGHT_HALF
        elif playerCentery - (cameray + WINDOW_HEIGHT_HALF) > CAMERA_SLACK :
            cameray = playerCentery - CAMERA_SLACK - WINDOW_HEIGHT_HALF

        DisplaySurf.fill(GRASS_COLOR)

        for gObj in grassObjs :
            gRect = pygame.Rect((gObj['x'] - camerax, 
                                 gObj['y'] - cameray,
                                 gObj['width'],
                                 gObj['height']))
            DisplaySurf.blit(GRASS_IMGS[gObj['grassImage']], gRect)

        for sObj in squirrelObjs :
            sObj['rect'] = pygame.Rect((sObj['x'] - camerax,
                                        sObj['y'] - cameray - GetBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                        sObj['width'],
                                        sObj['height']))
            DisplaySurf.blit(sObj['surface'], sObj['rect'])

        flashOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulneralMode and flashOn) :
            playerObj['rect'] = pygame.Rect((playerObj['x'] - camerax,
                                             playerObj['y'] - cameray - GetBounceAmount(playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
                                             playerObj['size'],
                                             playerObj['size']))
            DisplaySurf.blit(playerObj['surface'], playerObj['rect'])

        DrawHealthMeter(playerObj['health'])

        for event in pygame.event.get() :
            if event.type == QUIT :
                Terminate()

            elif event.type == KEYDOWN :
                if event.key in (K_UP, K_w) :
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s) :
                    moveDown = True
                    moveUp = False
                elif event.key in (K_LEFT, K_a) :
                    moveLeft = True
                    moveRight = False
                    if playerObj['facing'] == RIGHT :
                        playerObj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d) :
                    moveLeft = False
                    moveRight = True
                    if playerObj['facing'] == LEFT :
                        playerObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (playerObj['size'], playerObj['size']))
                    playerObj['facing'] = RIGHT
                elif winMode and event.key == K_r :
                    return
            elif event.type == KEYUP :
                if event.key in (K_LEFT, K_a) :
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d) :
                    moveRight = False
                elif event.key in (K_UP, K_w) :
                    moveUp = False
                elif event.key in (K_DOWN, K_s) :
                    moveDown = False
                elif event.key == K_ESCAPE :
                    Terminate()

        if not gameOverMode :
            if moveLeft :
                playerObj['x'] -= MOVERATE
            if moveRight :
                playerObj['x'] += MOVERATE
            if moveUp :
                playerObj['y'] -= MOVERATE
            if moveDown :
                playerObj['y'] += MOVERATE

            if (moveLeft or moveRight or moveUp or moveDown) or playerObj['bounce'] != 0 :
                playerObj['bounce'] += 1
            if playerObj['bounce'] > BOUNCERATE :
                playerObj['bounce'] = 0

            for i in range(len(squirrelObjs) - 1, -1, -1) :
                sqObj = squirrelObjs[i]
                if 'rect' in sqObj and playerObj['rect'].colliderect(sqObj['rect']) :
                    if sqObj['width'] * sqObj['height'] < playerObj['size'] ** 2 :
                        playerObj['size'] += int((sqObj['width'] * sqObj['height']) ** 0.2) + 1
                        del squirrelObjs[i]

                        if playerObj['facing'] == LEFT :
                            playerObj['surface'] = pygame.transform.scale(L_SQUIR_IMG, (playerObj['size'], playerObj['size']))
                        if playerObj['facing'] == RIGHT :
                            playerObj['surface'] = pygame.transform.scale(R_SQUIR_IMG, (playerObj['size'], playerObj['size']))

                        if playerObj['size'] > WINSIZE :
                            winMode = True
                    elif not invulneralMode : 
                        invulneralMode = True
                        invulneralStartTime = time.time()
                        playerObj['health'] -= 1
                        if playerObj['health'] == 0 :
                            gameOverMode = True
                            gameOverStartTime = time.time()
        else :
            DisplaySurf.blit(gameOverSurf, gameOverRect)
            if time.time() - gameOverStartTime > GAMEOVERTIME :
                return

        if winMode :
            DisplaySurf.blit(winSurf, winRect)
            DisplaySurf.blit(winSurf2, winRect2)

        pygame.display.update()
        FPSClock.tick(FPS)

def DrawHealthMeter(currentHealth) :
    for i in range(currentHealth) :
        pygame.draw.rect(DisplaySurf, RED, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH) :
        pygame.draw.rect(DisplaySurf, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)

def Terminate() :
    pygame.quit()
    sys.exit()

def GetBounceAmount(currentBounce, bounceRate, bounceHeight) :
    return int(math.sin(math.pi / float(bounceRate)) * currentBounce) * bounceHeight

def GetRandomVelocity() :
    speed = random.randint(SQUIRRELMINSPEED, SQUIRRELMAXSPEED)
    if random.randint(0, 1) == 0 :
        return speed
    else :
        return -speed

def GetRandomOffCameraPos(camerax, cameray, objWidth, objHeight) :
    cameraRect = pygame.Rect(camerax, cameray, WINDOW_WIDTH, WINDOW_HEIGHT)
    while True :
        x = random.randint(camerax - WINDOW_WIDTH, camerax + (2 * WINDOW_WIDTH))
        y = random.randint(cameray - WINDOW_HEIGHT, cameray + (2 * WINDOW_HEIGHT))
        
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not objRect.colliderect(cameraRect) :
            return (x, y)

def MakeNewSquirrel(camerax, cameray) :
    sq = {}
    generalSize = random.randint(5, 25)
    multiplier = random.randint(1, 3)
    sq['width'] = (generalSize + random.randint(0, 10)) * multiplier
    sq['height'] = (generalSize + random.randint(0, 10)) * multiplier
    (sq['x'], sq['y']) = GetRandomOffCameraPos(camerax, cameray, sq['width'], sq['height'])
    sq['movex'] = GetRandomVelocity()
    sq['movey'] = GetRandomVelocity()
    if sq['movex'] < 0 :
        sq['surface'] = pygame.transform.scale(L_SQUIR_IMG, (sq['width'], sq['height']))
    else :
        sq['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sq['width'], sq['height']))

    sq['bounce'] = 0
    sq['bouncerate'] = random.randint(10, 18)
    sq['bounceheight'] = random.randint(10, 50)

    return sq

def MakeNewGrass(camerax, cameray) :
    gr = {}
    gr['grassImage'] = random.randint(0, len(GRASS_IMGS) - 1)
    gr['width'] = GRASS_IMGS[0].get_width()
    gr['height'] = GRASS_IMGS[0].get_height()
    (gr['x'], gr['y']) = GetRandomOffCameraPos(camerax, cameray, gr['width'], gr['height'])
    gr['rect'] = pygame.Rect((gr['x'], gr['y'], gr['width'], gr['height']))

    return gr

def IsOutsideActiveArea(camerax, cameray, obj) :
    boundsleftEdge = camerax - WINDOW_WIDTH
    boundsTopEdge = cameray - WINDOW_HEIGHT

    boundsRect = pygame.Rect(boundsleftEdge, boundsTopEdge, WINDOW_WIDTH * 3, WINDOW_HEIGHT * 3)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    
    return not boundsRect.colliderect(objRect)

if __name__ == "__main__" :
    DoMain()
