#!/usr/bin/env python3


def BuildBoard( fileString ):

 fp = open( fileString, 'r')
 line = fp.readline()
 dim = line.split()
 w, h = int(dim[0]), int(dim[1])
 #w, h = width, height
 board = [['.' for y in range(h)] for x in range(w)]
 count = 0
 while line:
  line = fp.readline()
  if len(line) == 0: 
   break
  x = 0
  for char in range(len(line)):
   if char < w:
    if line[x] == ' ':
     pass
    elif line[x] == '\n' or line[x] == 0:
     pass
    else:
     board[x][count] = line[x]
     x += 1
  count += 1
 fp.close()
 
 return board