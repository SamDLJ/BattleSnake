#!/usr/bin/env python3
'''
https://oeis.org/A189722

The On-line Encyclopedia of Integer Sequences explains:

"Number of self-avoiding walks of length n on a square lattice such that 
at each point the angle turns 90 degrees (the first turn is assumed to be 
to the left - otherwise the number must be doubled)."

The encyclopedia mentions that 'Vi Hart came up with this idea of snakes' in one 
of her YouTube videos. Note the first 10 make a Fibonacci sequence, but after
that it diverges.

A189722:
1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 141, 226, 362, 580, 921, 1468, 2344, 
3740, 5922, 9413, 14978, 23829, 37686, 59770, 94882, 150606, 237947, 376784, 
597063, 946086, 1493497, 2361970, 3737699, 5914635, 9330438, 14741315, 23301716, 
36833270, 58071568, ...

===========



Can use this algorithm for battlesnake?
 'tight' counter-clockwise coiling

When looking at the actual path, the most visible features are:
 start and end
 long stretches or 'staircases' = ...0101010101...
  -four different directions
 'plus' patterns = ...0110110110... or ...1001001001...
  -four different directions
 vertical/horizontal 'castle walls' = ...00110011001100...
  -two different directions
  
could also turn into a tarsky carpet type thing.(?)

number of segments matters: even number is connectable, while odd is not



system is chaotic: no way to determine which direction the last segment is pointing
'''

import re




GRID_SIZE = 31
MAX_LENGTH = GRID_SIZE-1
grid = [[0]*GRID_SIZE for i in range(GRID_SIZE)]
S = int(GRID_SIZE/2)
grid[S][S] = 1
grid[S][S-1] = 1


def list_binary_strings(string_length):
 sList = []
 for b in range(0, 2**string_length):
  binary_format = format(b, "b")
  bs = str(binary_format).zfill(string_length)
  sList.append(bs)
 return sList

def print_list(L):
 for s in L:
  print(s)

def print_grid(g):
 for y in range(len(g[0])):
  for x in range(len(g)):
   print(g[x][y], end='')
  print()
 print()


def reset_grid(g):
 S = int(len(g[0])/2)
 for y in range(len(g[0])):
  for x in range(len(g)):
   g[x][y] = 0
 g[S][S] = 1
 g[S][S-1] = 1


def wiggle(grid, string):
 S = int(len(grid[0])/2)
 x = S
 y = S-1
 u = True
 d = False
 l = False
 r = False
 for c in string:
  if u:
   if c == '0':
    x -= 1
    l = True
   else:
    x += 1
    r = True
   u = False
  elif l:
   if c == '0':
    y += 1
    d = True
   else:
    y -= 1
    u = True
   l = False
  elif d:
   if c == '0':
    x += 1
    r = True
   else:
    x -= 1 
    l = True
   d = False
  elif r:
   if c == '0':
    y -= 1
    u = True
   else:
    y += 1
    d = True
   r = False
  if grid[x][y] == 1:
   reset_grid(grid)
   return False
  else:
   grid[x][y] = 1
 reset_grid(grid)
 return True  





def generate_sequence(n):
 for n in range(n):
  if n > 15:
   print("might take a long time...better stop")
   break
  sList = list_binary_strings(n)
  count = 0
  for s in sList:
   if wiggle(grid, s):
    count += 1
  print(int(count/2))

def valid_strings(n):
 if n > 15:
  print("might take a long time...better not")
  return []
 sList = []
 lbs = list_binary_strings(n)
 for s in lbs:
   if wiggle(grid, s):
    sList.append(s)
 return sList
 
#L = valid_strings(10)
#print_list(L)


def translate(string):
 startG = re.match("^001.*", string)
 startD = re.match("^010.*", string)
 startP = re.match("^011.*", string)
 startB = re.match("^100.*", string)
 startT = re.match("^101.*", string)
 startK = re.match("^110.*", string)
 
 endNG = re.match(".*$", string)
 #endN
 staircase = re.match(".*(10){2,}|(01){2,}", string)
 cross = re.match("\.LM ([+-])?(\d+)\s*$", string)
 vertwall = re.match("\.LM ([+-])?(\d+)\s*$", string)
 horzwall = re.match("\.LM ([+-])?(\d+)\s*$", string)
 if staircase:
  print("stairs")
 if cross:
  print("cross")
 

translate('00110')
translate('100111010101')