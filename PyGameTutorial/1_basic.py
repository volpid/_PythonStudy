#!/usr/bin/python3
# -*-coding-utf8-*-

import sys
import pygame
from pygame.locals import *

pygame.init()

windowsSurface = pygame.display.set_mode((800, 600), 0, 32)

while True :
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        pygame.display.update()

