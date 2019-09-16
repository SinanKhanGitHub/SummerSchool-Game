import math 
'''
This module provides access to the 
mathematical functions defined by the C standard.
'''
import random 
'''
This module implements pseudo-random 
number generators for various distributions.
'''
import pygame 
'''
Free and Open Source python programming 
language library for making multimedia applications like 
games built on top of the excellent SDL library
Needed pip install
'''
import tkinter as tk
'''
Tkinter Python's de-facto standard GUI (Graphical User
Interface) package. thin object-oriented layer on 
top of Tcl/Tk.
TK - independent windowing toolkit
'''
from tkinter import messagebox
'''
Tkinter tkMessageBox has various methods
to display a message box.
'''
# Starter code: We are going to build the classes of cube and snake now
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        pass
    def move(self, dirnx, dirny):
        pass
    def draw(self, surface, eyes=False):
        pass

# pass statement is a null operation, nothing happens when it executes

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        pass
        self.color = color
        self.head = cube(pos)  
        # The head will be the front of the snake
        self.body.append(self.head)
        '''  
        We will add head (which is a cube object) to our body list
        These will represent the direction our snake is moving
        '''
        self.dirnx = 0 
        self.dirny = 1
    def move(self):
        pass
    def reset(self, pos):
        pass
    def addCube(self):
        pass
    def draw(self, surface):
        pass

def drawGrid(width,rows,surface):
    sizeBtwn = width // rows  # Gives us the distance between the lines

    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y
    for l in range(rows):  
        # We will draw one vertical and one horizontal line each loop
        x = x + sizeBtwn
        # Means that the next x line will be the previous plus the size in between
        y = y + sizeBtwn
        # Means that the next y line will be the previous plus the size in between
        
        
        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))
        ''' pygame something in the module 
        '''

def redrawWindow(surface):
    global width, rows
    surface.fill((0,0,0))
    '''
    Fills screen with black (I believe the numbers are to give the color black)
    surface refers to the input
    fill is just text (apparently refers to a member)
    '''
    drawGrid(width,rows,surface)
    '''  
    Will draw out the grid lines
    surface refers to the input
    '''
    pygame.display.update() # Simply updates the screen


def randomSnack(rows, item):
    pass

def message_box(subject, content):
    pass

def main():
    global width, rows, s
    width = 500    # Width of our screen
    height = 500   # Height of our screen
    rows = 20      # Amount of rows

    win = pygame.display.set_mode((width,height)) 
    # Creates out screen object

    s = snake((255,0,0),(10,10)) 
    # Creates snake object which we wil code later

    clock = pygame.time.Clock() 
    # Creating a clock object

    flag = True
    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(50) 
        # This will delay the game so it doesnt run too quickly
        
        clock.tick(10) 
        # Will ensure our game runs at 10 FPS
        
        redrawWindow(win) 
        # This will refresh our screen

main()



