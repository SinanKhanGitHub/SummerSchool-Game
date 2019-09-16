#Snake Tutorial Python
import math
import random
import pygame

pygame.init()
#import tkinter as tk
#from tkinter import messagebox
#import time

rows = 30
one_row = rows // rows
ratio_header_to_screen = 0.1
width = 900 
white = (255,255,255)
purple = (150,111,214)
red = (255,0,0)
green = (0,255,0)
yellow = (253, 208, 35)
emerald = (31,78,48)
dark_green = (58,95,11)
pastel_green = (137,232,148)
black = (0,0,0)
win = pygame.display.set_mode((width, width))
img_apple = pygame.transform.scale(pygame.image.load('apple_original.png'),((width//rows),(width//rows)))
highscore = 0


class cube(object):
    rows = 30           # Changed from 500 * 20 to 1000 * 40
    w = 900
    def __init__(self,start,dirnx=1,dirny=0,color=purple):
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

        #if object = randomSnack():

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) 
        #pygame.draw.ellipse(surface, self.color, (i*dis+1,j*dis+1, dis+3, dis-2)) # Its been stretched out by 3, but problems remain with keeping the 'cubes' all together
        #Draws the cube proportional to the height and rows of the game itself and the color based on the functuon color above on the surface which is the game display
        #pygame.draw.circle(surface,self.color,(i*dis+dis//2-dis,j*dis+8),dis//2) # We have to change the snake to a circular object
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, yellow, circleMiddle, radius)
            pygame.draw.circle(surface, yellow, circleMiddle2, radius)
            pygame.draw.line(surface, red, (i*dis+dis//3,j*dis+4*dis//5),(i*dis-dis//3,j*dis+4*dis//5))
        

class snake(object):
    global s #rows, width # Added by new boston
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        #self.dirnx = 0 or 1 or -1   # Changed to add OR and number, diagonal movement
        #self.dirny = 0 or 1 or -1

    def move(self):
        for event in pygame.event.get():
            #print(event)                  # Adding history logging
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

                if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
                # Last 3 changed to IF functions to allow for diagonal movement
                # Removed 1 of the self dirns for each line to allow for diagonal movment
                # Might want to add function to turn around

        for i, c in enumerate(self.body):
            p = c.pos[:] # The colon means analyze everything e.g. [:-1] means 
            # everything till the last element, [:1] everything after first element 
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
        
    def crash(self): # Being added to stop snake at crash      
        self.dirnx = 1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        #s.body[0].pos = (10,10) This works but I want it to go back to the previous position
        

    def reset(self, pos):
        global score, highscore, increasing_score
        #centered_txt2_screen("You Lost!",(255,255,255)) # New Boston
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        if score >= highscore:
            highscore = score
        score = 0
        increasing_score = 1  
        
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

def rand(x_or_y): # added to create random X and Y values with specficity to what row/column something should be
        global difficulty
        if x_or_y == 'X':
            randX = random.randrange((one_row)*difficulty,rows-((one_row)*difficulty))
            return randX
        if x_or_y == 'Y':
            randY = random.randrange(rows * ratio_header_to_screen, rows-((one_row)*difficulty))
            return randY 
            # width needs to be replace with height in the future
    

'''
def score(score): # Adding from new boston PROBLEM: SMALL FONT IS NOT DEFINED
    text = smallfont.render("Score: " +str(score), True, color=(255,255,255))
    win.blit(text, [0,0])
'''

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0    # Width and rows *5 added to give the box above, changed to ratio_header_to_screen
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, green, (x, w * ratio_header_to_screen),(x,w-sizeBtwn*difficulty))     # Colors changed to white 0,0,0
        pygame.draw.line(surface, green, (sizeBtwn*difficulty, y + w * ratio_header_to_screen - sizeBtwn),(w - sizeBtwn*difficulty, y + w * ratio_header_to_screen  - sizeBtwn))
        

def redrawWindow(surface):
    global s, snack, score, positions_snack, highscore, difficulty  # Dont need rows or width, ratio_header_to_screen 
    #ratio_header_to_screen = 0.2 # Added because of New Boston
    border = width // rows # ratio'd to number of rows
    surface.fill(pastel_green, rect=[border*difficulty,width * ratio_header_to_screen, width - border*difficulty, width - width * ratio_header_to_screen])
    surface.fill(emerald,rect=[0,0, width, width * ratio_header_to_screen]) # Trying the big box
    surface.fill(emerald,rect=[0,width-border*difficulty, width, border*difficulty])
    surface.fill(emerald,rect=[0,width * ratio_header_to_screen, border*difficulty, width - width * ratio_header_to_screen])
    surface.fill(emerald,rect=[width-border*difficulty,width * ratio_header_to_screen, border*difficulty, width - width * ratio_header_to_screen]) # Bottom barrier New Boston
    centered_txt2_screen('Score '+str(score)+'    '+'Highscore '+str(highscore), white, 2, size=medfont)
    s.draw(surface)
    #snack.draw(surface) Dont need anymore
    surface.blit(img_apple, (rows * positions_snack[0],rows * positions_snack[1]))
    #drawGrid(width,rows,surface) #Looks better without
    pygame.display.set_caption('Sinans Snake Adventure')  
    #Added myself #score(score) # Adding from new boston 
    #win.blit(img_apple,(10,10)) # Works but the apple is too big the thing needs to be scaled down pixel wise
    pygame.display.update()



def start_screen(): #Taken from New Boston
    global difficulty
    intro = True
    while intro:
        win.fill(green)
        centered_txt2_screen("Speed Snake!", red, 3, size = bubblefont)
        centered_txt2_screen("Sinan Khan",black, 5, size = smallfont)
        centered_txt2_screen("Select a difficulty to begin", black, 15, size = medfont)
        centered_txt2_screen("E = Ekans         M = Snake        H = Arbok", black, 25, size = medfont)
        centered_txt2_screen("Move around with the arrow keys, (diagonal movement included!)",black, 29, size = smallfont)
        pygame.time.Clock().tick(15)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Added to ensure you can close the game at all times
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_e]:
                    difficulty = 1
                    main()
                    intro = False
                elif keys[pygame.K_m]:
                    difficulty = 2
                    main()
                    intro = False
                elif keys[pygame.K_h]:
                    difficulty = 3
                    main()
                    intro = False
                    break



def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange((one_row)*difficulty,rows-((one_row)*difficulty)) # Need to change so that it doesnt come on header or off page 
        y = random.randrange(rows * ratio_header_to_screen, rows-((one_row)*difficulty))
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break  
    return (x,y)

   
    

# Set of fonts used for all text displayed
# I wanna clean this up so that it pulls the font out of a table

smallfont = pygame.font.Font('OpenSans-Light.ttf', 25)
medfont = pygame.font.Font("Roboto-ThinItalic.ttf", 50)
largefont = pygame.font.Font("PlayfairDisplaySC-BoldItalic.otf", 75)
bubblefont = pygame.font.Font("Bubblegum.ttf", 75)

'''
def text_objects(text, color, size): # added font here
    if size == "small":
        textSurf = smallfont.render(text, True, color)
    elif size == "medium":
        textSurf = medfont.render(text, True, color)
    elif size == "large":
        textSurf = largefont.render(text, True, color)
    return textSurf, textSurf.get_rect()  
    #for strx in type: # added this on test basis not sure if it will work
    #textSurf = xfont.render(text, True, color) # font changed to x


def centered_txt2_screen(text,color, y_displace=0, size="smallfont"): #font=small_font):
     t = text_objects(text,color,size)
     r = text_objects(text,color,size). #textSurf is just like pygame surf, textRect
     textRect.center = (width // 2), (width // 2) + y_displace # aimed to get the message away
     a = win.blit(textSurf, textRect)
     ''''''
     screen_text = font.render(msg, True, color) #this was the old uncentered text
     a = win.blit(screen_text, (250, 250))
     ''''''
     pygame.display.update(a)
     # pygame.time.wait(2000) # In milliseconds delays the program # The new boston
    
'''


def text_objects(text, color, size): # added font here
    if size == smallfont:
        textSurface = smallfont.render(text, True, color)
        return textSurface, textSurface.get_rect()  
    elif size == medfont:
        textSurface = medfont.render(text, True, color)
        return textSurface, textSurface.get_rect()  
    elif size == largefont:
        textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect() 
    elif size == bubblefont:
        textSurface = bubblefont.render(text, True, color)
        return textSurface, textSurface.get_rect() 
    #for strx in type: # added this on test basis not sure if it will work
    #textSurf = xfont.render(text, True, color) # font changed to x """

 

def centered_txt2_screen(msg,color, row_nr=rows//2,size=smallfont): #font=small_font):
    textSurf, textRect = text_objects(msg, color, size) #font)  #textSurf is just like pygame surf, textRect
    textRect.center = (width // 2), (row_nr * (width // rows)) # aimed to get the message away
    win.blit(textSurf, textRect)
    '''
    screen_text = font.render(msg, True, color) #this was the old uncentered text
    a = win.blit(screen_text, (250, 250))
    '''
    #pygame.display.update(a)
    # pygame.time.wait(2000) # In milliseconds delays the program # The new boston




'''
DONT NEED THIS
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
       pass
'''

def main():
    global width, s, snack, surface, score, positions_snack, highscore, difficulty #rows
    score = 0 
    increasing_score = 1 * difficulty
    #width = 750   # Changed from 500 * 20 to 1000 * 40 to 750 * 30
    #rows = 30
    #win = pygame.display.set_mode((width, width)) better to have win outside
    s = snake(purple, (rand('X'),rand('Y'))) 
    #s_2 = snake((0,255,0),(10,10))
    positions_snack = (randomSnack(rows,s))
    snack = cube(positions_snack,color=red)

    #pygame.display.update(pygame.transform.scale(win.blit(img_apple,randomSnack(rows, s)),(60,60))) # Trying to put the damn apple in 
    gameOn = True
    gameOver = False
    clock = pygame.time.Clock()


    while gameOn:
        FPS = 20 + 10*(difficulty) # Try fluid movement
        pygame.time.delay(0)       # Changed to 0 from 50
        clock.tick(FPS)       # Changed to 40 from 10
        s.move()
        #s_2.move()  
        #print(len(s.body))
        if gameOver == True: # Added by the new boston to allow for game over 
            s.reset((100,100))
            centered_txt2_screen("Game Over!", red, 10, size = bubblefont)
            centered_txt2_screen("Try again?              or too much 'bite'?", white, 15, size = medfont)
            centered_txt2_screen("P = Play Again!         T = Till Later!", black, 25, size = medfont)
            pygame.display.update()
            #s.reset((rand('X'),rand('Y')))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Added to ensure you can close the game at all times
                    pygame.quit()
                keys = pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_t]:
                        pygame.quit()
                        gameOver = False
                    elif keys[pygame.K_p]:
                        s.reset((rand('X'),rand('Y')))
                        positions_snack = randomSnack(rows, s)
                        snack = cube(positions_snack,color=red)
                        gameOver = False
                        break

        if s.body[0].pos == snack.pos:
            score = score + increasing_score
            increasing_score = increasing_score + 1
            s.addCube()
            positions_snack = randomSnack(rows, s)
            snack = cube(positions_snack,color=red)
            continue

        if s.body[0].pos  + (0,one_row) == snack.pos:
            score = score + increasing_score
            increasing_score = increasing_score + 1
            s.addCube()
            positions_snack = randomSnack(rows, s)
            snack = cube(positions_snack,color=red)
            continue

        if s.body[0].pos + (one_row,0) == snack.pos:
            score = score + increasing_score
            increasing_score = increasing_score + 1
            s.addCube()
            positions_snack = randomSnack(rows, s)
            snack = cube(positions_snack,color=red)
            continue

        if s.body[0].pos  + (one_row,one_row) == snack.pos:
            score = score + increasing_score
            increasing_score = increasing_score + 1
            s.addCube()
            positions_snack = randomSnack(rows, s)
            snack = cube(positions_snack,color=red)
            continue
            
        elif s.body[0].pos[0] <= (one_row) * difficulty - one_row:
            gameOver = True
            continue
            #s.reset((rand('X'),rand('Y'))) # Working solutoon
            
        elif s.body[0].pos[0] >= rows - (one_row) * difficulty: # Added by new boston, 
            #some issue with being able to leave at the bottom of the screen
            gameOver = True
            continue

        elif s.body[0].pos[1] <= rows * ratio_header_to_screen - (one_row): # Added by new boston, 
            #some issue with being able to leave at the bottom of the screen
            gameOver = True
            continue
            #s.reset((rand('X'),rand('Y'))) # Working solutoon
            
        elif s.body[0].pos[1] >= rows - (one_row)*difficulty: # Added by new boston, 
            #some issue with being able to leave at the bottom of the screen
            gameOver = True
            continue
        
        for g in range(len(s.body)):
            if s.body[g].pos in list(map(lambda z:z.pos,s.body[g+1:])):
                main()
                if highscore >= score:
                    highscore = score
                break
            continue

                #print(list(map(lambda z:z.pos,s.body[x+1:])))
                #print(s.body[x].pos)
                #print('Score: ', len(s.body))
                #message_box('You Lost!', 'Play again...')
                # centered_txt2_screen("You Lost!",red)
                # s.reset((rand('X'),rand('Y')))
                # break
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
start_screen()

