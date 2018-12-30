#!/usr/bin/env python3

# Snake Sprites



# update rect.x and rect.y (actual sprite image) according to their .myBoard
import pygame
from random import randint
from SnakeSettings import *


Apples = [[0]*20 for i in range(20)]

class Apple(pygame.sprite.Sprite):
 def __init__(self, x, y, Game):
  pygame.sprite.Sprite.__init__(self)
  global Apples
  self.Game = Game
  self.type = 'apple'
  self.SnakeSpeak = self.Game.fsb.render('', False, (255, 255, 255))
  self.image = pygame.Surface((size-8, size-8))
  self.image.fill(RED)
  self.rect = self.image.get_rect()
  self.rect.x = x*size+4
  self.rect.y = y*size+4
  self.X, self.Y = int(self.rect.x/size), int(self.rect.y/size)
  Apples[self.X][self.Y] = 1
  
 def update(self):
  #timer? could change colour
  pass
 



# represents the head of the snake
class Snake(pygame.sprite.Sprite):
 def __init__(self, x,y, Game):
  pygame.sprite.Sprite.__init__(self)
  self.myBoard = [[0]*20 for i in range(20)]
  self.Game = Game
  self.image = pygame.Surface((size, size))
  self.r, self.g, self.b = randint(150, 200), randint(150, 200), randint(150, 200)
  self.image.fill((self.r,self.g,self.b))
  self.rect = self.image.get_rect()
  self.rect.x, self.rect.y = x*size, y*size
  
  self.name = randomName()
  self.type = 'head'
  self.rank = 0
  
  self.X, self.Y = int(self.rect.x/size), int(self.rect.y/size)
  self.Segments = [self]
  a = BodySegment(self.Game, self)
  b = BodySegment(self.Game, self)
  self.NextSeg = a
  
  #print(self.Segments)
  
  self.myBoard[self.X][self.Y] = 2
  self.Attack = len(self.Segments)
  self.allowRight = True
  self.allowDown = True 
  self.allowLeft = True
  self.allowUp = True
  self.health = 100
  self.SnakeSpeak = self.Game.fsb.render(str(self.health), False, (self.r+50, self.g+50, self.b+50))

 def update(self):
  # ============================
  M = GET_NEXT_MOVE(self)
  # ============================
  oldX, oldY = self.X, self.Y # +1 is because body segment is smaller than head
  self.X, self.Y = MOVE(M, self.X, self.Y)
  self.myBoard[self.X][self.Y] = 2
  self.NextSeg.move(oldX, oldY) #recursive, pass the old position down the chain of segments
  self.health -= 1
  
  self.rect.x, self.rect.y = self.X*size, self.Y*size
   
  self.SnakeSpeak = self.Game.fsb.render(str(self.health), False, (self.r+50, self.g+50, self.b+50))
  
 def grow(self):
  g = BodySegment(self.Game, self)
  self.Attack += 1
  self.health = 100
  add_apple(self.Game)
  
  

#If head is 0, then next segment is 1, then 2, etc
class BodySegment(pygame.sprite.Sprite):
 def __init__(self, Game, Snake):
  pygame.sprite.Sprite.__init__(self)
  self.Game = Game
  self.Snake = Snake
  self.image = pygame.Surface((size-2, size-2))
  self.r, self.g, self.b = self.Snake.r-70, self.Snake.g-70, self.Snake.b-70 
  self.image.fill((self.r, self.g, self.b))
  self.rect = self.image.get_rect()
  self.rect.x, self.rect.y = -16, -16 #=== off screen at first
  self.type = 'body'
  self.rank = len(self.Snake.Segments) #rank calculated before appending
  self.X, self.Y = self.Snake.X, self.Snake.Y
  
  self.NextSeg = None
  self.Snake.Segments.append(self)
  self.Game.allSprites.add(self)
  self.Snake.Segments[self.rank-1].NextSeg = self # latch onto chain
  
  
  self.ReadyToMove = False
  self.SnakeSpeak = self.Game.fsb.render('', False, (WHITE))
  
 def move(self, x, y):
  if not self.ReadyToMove:
   self.ReadyToMove = True
   self.X, self.Y = x, y #int(self.rect.x/size), int(self.rect.y/size)
   self.Game.allSegments.add(self)
   self.Snake.myBoard[self.X][self.Y] = 1 # snake head has already moved one space
   # dont blit to surface yet!

  else:
   xNext, yNext = self.X, self.Y # old positions of this segment, to be passed down
   self.X, self.Y = x, y
   
   if self.NextSeg != None:
    self.NextSeg.move(xNext, yNext) # give the current position to the next segment
    self.Snake.myBoard[self.X][self.Y] = 1
   
   else:
    if self.Snake.myBoard[xNext][yNext] != 2:
     self.Snake.myBoard[xNext][yNext] = 0
   self.rect.x, self.rect.y = x*size+1, y*size+1 
   

# ==================== THE ART OF WAR ========================
# In the real tournament, parameters of functions might need to change
# 
def GET_NEXT_MOVE(Snake):

 check_walls(Snake)
 
 #check_next_to(Snake)
 
 #check_2_away(Snake)
 
 move = choose_random_direction(Snake, Snake.Game) # parameters might need to change
 
 return move
# ============================================================


# ============================================================
def check_walls(Snake):
 if Snake.rect.midbottom[1] >= screenHeight:
  Snake.allowDown = False
 else:
  Snake.allowDown = True
 if Snake.rect.midleft[0] <= 0:
  Snake.allowLeft = False
 else:
  Snake.allowLeft = True
 if Snake.rect.midright[0] >= screenWidth:
  Snake.allowRight = False
 else:
  Snake.allowRight = True
 if Snake.rect.midtop[1] <= 0:
  Snake.allowUp = False
 else:
  Snake.allowUp = True
# ============================================================








def MOVE(M, SX, SY):
 newX = SX
 newY = SY
 if M == 'right':
  newX = SX+1
 elif M == 'left':
  newX = SX-1
 elif M == 'up':
  newY = SY-1
 elif M == 'down':
  newY = SY+1
 return newX, newY
 

def add_apple(Game):
 x = randint(0, 19)
 y = randint(0, 19)
 newApple = Apple(x, y, Game)
 Game.allSprites.add(newApple)
 Game.allApples.add(newApple)
 


def pBoard(g):
 for y in range(len(g[0])):
  for x in range(len(g)):
   print(g[x][y], end='')
  print()
 print()





# BAD ALGORITHM! ======= dont use this, just for testing =======
def choose_random_direction(Snake, Game):
 move = 'up'
 found_a_direction = False
 waitTimer = 10
 while not found_a_direction and waitTimer >= 0:
  waitTimer -= 1
  r = randint(0, 3)
  
  if r == 0 and Snake.allowRight:
   if Snake.myBoard[Snake.X+1][Snake.Y] != 1:
    move = 'right'
    Snake.allowRight, Snake.allowDown, Snake.allowLeft, Snake.allowUp = False, True, True, True
    found_a_direction = True
  elif r == 1 and Snake.allowDown:
   if Snake.myBoard[Snake.X][Snake.Y+1] != 1:
    move = 'down'
    Snake.allowRight, Snake.allowDown, Snake.allowLeft, Snake.allowUp = True, False, True, True
    found_a_direction = True
  elif r == 2 and Snake.allowLeft:
   if Snake.myBoard[Snake.X-1][Snake.Y] != 1:
    move = 'left'
    Snake.allowRight, Snake.allowDown, Snake.allowLeft, Snake.allowUp = True, True, False, True
    found_a_direction = True
  elif r == 3 and Snake.allowUp:
   if Snake.myBoard[Snake.X][Snake.Y-1] != 1:
    move = 'up'
    Snake.allowRight, Snake.allowDown, Snake.allowLeft, Snake.allowUp = True, True, True, False
    found_a_direction = True 
   
 if waitTimer <= 0:
  print(Snake.name, "ran into something")
  #pBoard(Snake.myBoard)
  for seg in Snake.Segments:
   seg.kill()
  Snake.kill()
  #Game.DEAD = True
  
 return move
