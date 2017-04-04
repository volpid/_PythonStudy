#!/usr/bin/python3
# -*-coding-utf8-*-

import random
import pygame
import sys
import time
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30
FLASH_SPEED = 500
FLASH_DELAY = 200
BUTTON_SIZE = 200
BUTTON_GAP_SIZE = 20
TIMEOUT = 4
BASICFONTSIZE = 16

#RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (155, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 155, 0)
BRIGHT_GREEN = (0, 255, 0)
BLUE = (0, 0, 155)
BRIGHT_BLUE = (0, 0, 255)
YELLOW = (155, 155, 0)
BRIGHT_YELLOW = (255, 255, 0)
DARK_GREY = (40, 40, 40)

bgColor = BLACK

XMARGIN = int((WINDOW_WIDTH - (BUTTON_SIZE * 2 + BUTTON_GAP_SIZE)) / 2)
YMARGIN = int((WINDOW_HEIGHT - (BUTTON_SIZE * 2 + BUTTON_GAP_SIZE)) / 2)

YELLOW_RECT = pygame.Rect(XMARGIN, YMARGIN, BUTTON_SIZE, BUTTON_SIZE)
BLUE_RECT = pygame.Rect(XMARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, YMARGIN, BUTTON_SIZE, BUTTON_SIZE)
RED_RECT = pygame.Rect(XMARGIN, YMARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)
GREEN_RECT = pygame.Rect(XMARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, YMARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)

def DoMain() :
    global FPSClock
    global DisplaySurf
    global BasicFont
    global Beep1
    global Beep2
    global Beep3
    global Beep4

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulate")
    BasicFont = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    infoSurf = BasicFont.render("Match the pattern by clicking on the button or using the Q W A S keys", 1, DARK_GREY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOW_HEIGHT - 25)

    #load sound files
    Beep1 = pygame.mixer.Sound("./_Resource/beep1.ogg")
    Beep2 = pygame.mixer.Sound("./_Resource/beep2.ogg")
    Beep3 = pygame.mixer.Sound("./_Resource/beep3.ogg")
    Beep4 = pygame.mixer.Sound("./_Resource/beep4.ogg")

    pattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0
    waitingForInput = False

    while True:
        clickedButton = None
        DisplaySurf.fill(bgColor)

        DrawButtons()

        scoreSurf = BasicFont.render("Score " + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOW_WIDTH - 100, 10)

        DisplaySurf.blit(scoreSurf, scoreRect)

        CheckForQuit()

        for event in pygame.event.get() :
            if event.type == MOUSEBUTTONUP :
                (mousex, mousey) = event.pos
                clickedButton = GetButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN :
                if event.key == K_q :
                    clickedButton = YELLOW
                elif event.key == K_w :
                    clickedButton = BLUE
                elif event.key == K_a :
                    clickedButton = RED
                elif event.key == K_s :
                    clickedButton = GREEN

        if not waitingForInput :
            #play pattern
            pygame.display.update()
            pygame.time.wait(100)

            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern :
                FlashButtonAnimation(button)
                pygame.time.wait(FLASH_DELAY)
            waitingForInput = True
        else :
            if clickedButton and clickedButton == pattern[currentStep] :
                FlashButtonAnimation(clickedButton)
                currentStep += 1
                score += 1
                lastClickTime = time.time()

                if currentStep == len(pattern) :
                    ChangeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime) :
                GameoverAnimation()
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)

                ChangeBackgroundAnimation()

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

def FlashButtonAnimation(color, animationSpeed = 50) :
    if color == YELLOW :
        sound = Beep1
        flashColor = BRIGHT_YELLOW
        rectangle = YELLOW_RECT
    elif color == RED :
        sound = Beep2
        flashColor = BRIGHT_RED
        rectangle = RED_RECT
    elif color == BLUE :
        sound = Beep3
        flashColor = BRIGHT_BLUE
        rectangle = BLUE_RECT
    elif color == GREEN :
        sound = Beep4
        flashColor = BRIGHT_GREEN
        rectangle = GREEN_RECT

    origSurf = DisplaySurf.copy()
    flashSurf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
    flashSurf = flashSurf.convert_alpha()
    (r, g, b) = flashColor
    sound.play()

    for (start, end, step) in ((0, 255, 1), (255, 0, -1)) :
        for alpha in range(start, end, animationSpeed * step) :
            CheckForQuit()

            DisplaySurf.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DisplaySurf.blit(flashSurf, rectangle.topleft)
            
            pygame.display.update()
            FPSClock.tick(FPS)

        DisplaySurf.blit(origSurf, (0, 0))

def DrawButtons() :
    pygame.draw.rect(DisplaySurf, YELLOW, YELLOW_RECT)
    pygame.draw.rect(DisplaySurf, RED, RED_RECT)
    pygame.draw.rect(DisplaySurf, BLUE, BLUE_RECT)
    pygame.draw.rect(DisplaySurf, GREEN, GREEN_RECT)

def ChangeBackgroundAnimation(animationSpeed = 40) :
    global bgColor

    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    (r, g, b) = newBgColor

    for alpha in range(0, 255, animationSpeed) :
        CheckForQuit()
        DisplaySurf.fill(bgColor)
        
        newBgSurf.fill((r, g, b, alpha))
        DisplaySurf.blit(newBgSurf, (0, 0))

        DrawButtons()

        pygame.display.update()
        FPSClock.tick(FPS)

    bgColor = newBgColor

def GameoverAnimation(color = WHITE, animationSpeed = 50) :
    origSurf = DisplaySurf.copy()
    flashSurf = pygame.Surface(DisplaySurf.get_size())
    flashSurf = flashSurf.convert_alpha()
    Beep1.play()
    Beep2.play()
    Beep3.play()
    Beep4.play()

    (r, g, b) = color
    for i in range(3) :
        for (start, end, step) in ((0, 255, 1), (255, 0, -1)) :
            for alpha in range(start, end, animationSpeed * step) :
                CheckForQuit()
                flashSurf.fill((r, g, b, alpha))
                DisplaySurf.blit(origSurf, (0, 0))
                DisplaySurf.blit(flashSurf, (0, 0))
                DrawButtons()
                
                pygame.display.update()
                FPSClock.tick(FPS)

def GetButtonClicked(x, y) :
    if YELLOW_RECT.collidepoint(x, y) :
        return YELLOW
    elif RED_RECT.collidepoint(x, y) :
        return RED
    elif GREEN_RECT.collidepoint(x, y) :
        return GREEN
    elif BLUE_RECT.collidepoint(x, y) :
        return BLUE

    return None

if __name__ == "__main__" :
    DoMain()
