#!/usr/bin/env python3

# SnakeTester
#


import pygame
import sys
from SnakeSettings import *
from SnakeSprites import *
from BuildBoard import BuildBoard



class Game:
 def __init__(self):
  pygame.init()
  
  # returns None for some reason?
  FONTS = pygame.font.get_fonts()
  for f in FONTS:
   print(f)
  
  self.screen = pygame.display.set_mode((screenWidth*SCALE, screenHeight*SCALE))
  pygame.display.set_caption(TITLE)
  self.CLOCK = pygame.time.Clock()
  self.running = True
  self.DEAD = False
  self.bh = 0
  self.bw = 0
  self.fsb = pygame.font.SysFont('freesansbold.ttf', 18)
  #self.fsb = pygame.font.SysFont('arial', 20)
  
  
  #self.SnakeHeads = [[0]*20 for i in range(20)]
  
  
 def update(self):
  self.allSprites.update()
  
  XY = []
  melee = []
  #===== Check Health and add add to coordinate list
  segBoard = [[0]*20 for i in range(20)]
  for seg in self.allSegments:
   segBoard[seg.X][seg.Y] = 1
   
  for s in self.allSnakes:
   if segBoard[s.X][s.Y] == 1:
    for seg in s.Segments:
     seg.kill()
    s.kill()
    print(s.name, "ran into a snake")
   if s.health == 0:
    for seg in s.Segments:
     seg.kill()
    s.kill()
    print(s.name, "starved to death")
   XY.append((s.X,s.Y))
  
     
  
  #===== If there are any duplicate x,y pairs, it means more than 1 snake are on a square
  dups = set([xy for xy in XY if XY.count(xy) > 1]) # grab all the duplicates
  if dups:
   for s in self.allSnakes:
    if (s.X,s.Y) in dups:
     melee.append(s) #set up for resolving battle
   for i in range(len(melee)-1):
    for j in range(i+1, len(melee)):
     if melee[i].Attack > melee[j].Attack:
      print(melee[i].name, " killed ", melee[j].name)
      for seg in melee[j].Segments:
       seg.kill()
      melee[j].kill()
     elif melee[i].Attack == melee[j].Attack:
      print(melee[i].name, " and ", melee[j].name, " killed each other")
      for seg in melee[i].Segments:
       seg.kill()
      melee[i].kill()
      for seg in melee[j].Segments:
       seg.kill()
      melee[j].kill()
     elif melee[i].Attack < melee[j].Attack: 
      print(melee[j].name, " killed ", melee[i].name)
      for seg in melee[i].Segments:
       seg.kill()
      melee[i].kill()
  
  for a in self.allApples:
   for s in self.allSnakes:
    if (s.X, s.Y) == (a.X, a.Y):
     print(s.name, "got an apple")
     a.kill()
     s.grow()
     
  if len(self.allSnakes) == 0:
   self.DEAD = True

 def events(self):
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    self.playing = False
    self.running = False
  if self.DEAD:
   self.playing = False
   self.running = False
   print("no snakes left!")
    
 def draw(self):
  self.screen.fill(BLACK)
  self.allSprites.draw(self.screen)
  #self.allApples.draw(self.screen)
  
  for s in self.allSprites:
   if s.rect.y == 0:
    self.screen.blit(s.SnakeSpeak, (s.rect.x,s.rect.y+20))
   else:
    self.screen.blit(s.SnakeSpeak, (s.rect.x,s.rect.y-12))

  pygame.display.flip()
  
  
  
  
  
 def NewGame(self):
  self.allSprites = pygame.sprite.Group()
  self.allSnakes = pygame.sprite.Group()
  self.allApples = pygame.sprite.Group()
  self.allSegments = pygame.sprite.Group()
  self.initializeBoard()
  self.run()
  
 def initializeBoard(self):
  boardInit = BuildBoard( 'board.txt' )
  
  self.bh = len(boardInit[0])
  self.bw = len(boardInit)
  #self.BoardStates = [['.'] * bh for i in range(bw)]
  
  for y in range( self.bh ):
   for x in range( self.bw ):
    #print(boardInit[x][y], end='')
    
    if boardInit[x][y] == 'W':
     wSnek = Snake(x, y, self)
     #self.BoardStates[x][y] = 'W'
     self.allSprites.add(wSnek)
     self.allSnakes.add(wSnek)
      
    elif boardInit[x][y] == 'a':
     apple = Apple(x, y, self)
     #self.BoardStates[x][y] = 'o'
     self.allSprites.add(apple)
     self.allApples.add(apple)
    
    elif boardInit[x][y] == 'E':
     enemySnek = Snake(x, y, self)
     #self.BoardStates[x][y] = 'E'
     self.allSprites.add(enemySnek)
     self.allSnakes.add(enemySnek)
     
   #print()
  #DF = pygame.font.get_default_font()
  #print(DF)
  
 
 def run(self):
  self.playing = True
  while self.playing:
   self.CLOCK.tick(FPS)
   self.events()
   self.update()
   self.draw()

 
     
g = Game()
while g.running:
 g.NewGame()
pygame.quit()


