#!/usr/bin/python3
# -*-coding-utf8-*-

import sys
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("pygame basic")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)

FPS = 30
fpsClokc = pygame.time.Clock()

catImage = pygame.image.load("_Resource/cat.png")
catx = 10
caty = 10

directions = ["right", "left", "up", "down"]
direction = directions[0]

windowsSurface = pygame.display.set_mode((800, 600), 0, 32)

#pygame.draw.polygon(windowsSurface, BLACK, ((100, 100), (100, 200), (200, 100), (200, 200)), 2)
#pygame.draw.line(windowsSurface, RED, (0, 0), (400, 300), 4)

#pixelArr = pygame.PixelArray(windowsSurface)
#pixelArr[150][150] = RED
#pixelArr[150][151] = GREEN
#pixelArr[151][150] = GREEN
#pixelArr[320][320] = BLUE

#print(pixelArr[100][100])
#print(pixelArr[0][0])
#print(pixelArr[100][150])

#del pixelArr

while True :
    windowsSurface.fill(WHITE)
    
    if direction == directions[0] :
        catx += 5
        if catx > 400 :
            direction = directions[2]

    elif direction == directions[1] :
        catx -= 5
        if catx < 10 :
            direction = directions[3]

    elif direction == directions[2] :
        caty += 5
        if caty > 500 :
            direction = directions[1]

    elif direction == directions[3] :
        caty -= 5
        if caty < 10 :
            direction = directions[0]

    windowsSurface.blit(catImage, (catx, caty))

    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    
    pygame.display.update()

    fpsClokc.tick(FPS)

