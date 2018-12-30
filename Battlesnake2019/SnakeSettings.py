#!/usr/bin/env python3


# SnakeSettings
#

import pygame
from random import randint

TITLE = "Wyrmhol"

SCALE = 1
size = 16
screenWidth = 20*size
screenHeight = 20*size

FPS = 10

#BG = pygame.image.load("marioGrass.png")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,50,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
DARKYELLOW = (100,100,0)
PURPLE = (100,0,100)

def randomName():
 first = ["Big ", "Mr ", "Danger ", "Super ", "Jam ", "Green ", "Lazer ", "Mon ", "Ping ","Zoom ","Doom ","Zan ","Py ","Long ","Death "]
 last = ["Zam", "Train", "Noodle", "Snack", "Face", "Snek", "Zoid","Tron","Zoop","Squaz"]
 
 fn = randint(0, len(first)-1)
 ln = randint(0, len(last)-1)
 
 name = first[fn]+""+last[ln]
 
 return name
 