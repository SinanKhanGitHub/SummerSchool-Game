#Snake Tutorial Python
import math
import random
import pygame
LOL = pygame.init()
print(LOL)
import tkinter as tk
from tkinter import messagebox
import time

rows = 30
w = 750 
width = 900 

ratio = rows // 6

class cube(object):
    rows = 30           # Changed from 500 * 20 to 1000 * 40
    w = 750
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 0       # Changed to 0
        self.dirny = 0       # Need this because we need the direction to change not the speed to change based on the number of times clicked on keyboard
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) 
        #Draws the cube proportional to the height and rows of the game itself and the color based on the functuon color above on the surface which is the game display
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        

class snake(object):
    # global s, rows, width # Added by new boston
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        #self.dirnx = 0 or 1    # Changed to add OR and number, diagonal movement
        #self.dirny = 0 or 1

    def move(self):
        for event in pygame.event.get():
            print(event)                  # Adding history logging
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
                # Last 3 changed to IF functions to allow for diagonal movement
                # Removed 1 of the self dirns for each line to allow for diagonal movment
        
            
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
        
        
        
        

    def reset(self, pos):
        #message_to_screen("You Lost!",(255,255,255)) # New Boston
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        #self.dirnx = 0   Because we want to allow diagonal movement
        #self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        elif dx == -1 and dy == -1:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]+1)))
        elif dx == 1 and dy == 1:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]-1)))
        elif dx == 1 and dy == -1:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1]+1)))
        elif dx == -1 and dy == 1:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1]-1)))
        #Added these to allow for diagonal movement and addition of cubes but the thing still fucks up and returns back to square 1
        # Need to check later with a print score/reset function

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy # May need to change this
        
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

'''
def score(score): # Adding from new boston PROBLEM: SMALL FONT IS NOT DEFINED
    text = smallfont.render("Score: " +str(score), True, color=(255,255,255))
    win.blit(text, [0,0])
'''

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0 + rows * 5 
    y = 0 + rows * 5       # Width and rows *5 added to give the box above
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))     # Colors changed to white 0,0,0
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def redrawWindow(surface):
    global rows, width, s, snack, ratio
    ratio = rows // 6
    surface.fill((0,0,0))
    surface.fill((255,0,0),rect=[0,0, width, rows * ratio]) # Trying the big box
    surface.fill((255,0,0),rect=[0,width-5, width, rows * 1]) # Bottom barrier New Boston
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.set_caption('Sinans Snake Adventure')  
    #Added myself #score(score) # Adding from new boston 
    pygame.display.update()



def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

"""
def text_screen(text,color,x,y):
    screen_text = font.render(text, True, color)
    win.blit(screen_text, [x,y])
"""

font = pygame.font.SysFont(None, 25)
def message_to_screen(msg,color):
    global win
    screen_text = font.render(msg, True, color)
    a = win.blit(screen_text, (250, 250))
    pygame.display.update(a)
    # pygame.time.wait(2000) # In milliseconds delays the program # The new boston
    
    
    
    



def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
       pass

def main():
    global width, rows, s, snack, win
    score = 0
    increasing_score = 1
    #width = 750   # Changed from 500 * 20 to 1000 * 40 to 750 * 30
    #rows = 30
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
    gameOver = False

    clock = pygame.time.Clock()
    
    while flag:
        if gameOver == True:
            message_to_screen("Game over, press C to play again or Q to Quit", (255,0,0))
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_q]:
                        gameOver = False
                        pygame.quit()
                    if keys[pygame.K_c]:
                        gameOver = False
                        #s.reset((10,10)) Try without reset
                        break

        FPS = 15
        pygame.time.delay(0)       # Changed to 0 from 50
        clock.tick(FPS)       # Changed to 40 from 10
        s.move()
        print(s.body[0].pos)
        if s.body[0].pos == snack.pos:
            score = score + increasing_score
            increasing_score = increasing_score + 1
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        
        
        if s.body[0].pos[1] <= ratio: # Added by new boston
            gameOver = True
            #s.reset((10,10)) Try without reset
            continue 
        

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #print(list(map(lambda z:z.pos,s.body[x+1:])))
                #print(s.body[x].pos)
                #print('Score: ', len(s.body))
                #message_box('You Lost!', 'Play again...')
                message_to_screen("You Lost!")
                s.reset((10,10))
                break
        '''
        for x in range(len(s.body)):
            if s.body[x].pos in (0,0):
                #print('Score: ', len(s.body))
                #message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break
        '''
        

            # Removing message box
        redrawWindow(win)

main()