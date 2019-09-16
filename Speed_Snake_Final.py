# Import needed modules
import math
import random
import pygame
pygame.init()


# Initial variables
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
pygame.display.set_caption('Sinans Speed Snake')  
img_apple = pygame.transform.scale(pygame.image.load('apple_original.png'),((width//rows),(width//rows)))
highscore = 0


# The cube is the building block of the snake and its added cubes
class cube(object):
    rows = 30           
    w = 900
    def __init__(self,start,dirnx=1,dirny=0,color=purple):
        self.pos = start
        self.dirnx = 0       # Set to zero to start the snake NOT moving
        self.dirny = 0      
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) # Allows for drawing cube
        
        if eyes:         # Allows for drawing the eyes as small circles on a 'given' cube
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, yellow, circleMiddle, radius)
            pygame.draw.circle(surface, yellow, circleMiddle2, radius)
        

class snake(object):
    global s
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

    def move(self):
        for event in pygame.event.get():
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
            
            '''To allow for diagonal movement:
                - initial self dirns removed
                - 'key' code changed to IF from elif
                - Removed 1 of the self dirns for each line to allow for diagonal movment'''

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

    def reset(self, pos):
        global score, highscore, increasing_score, difficulty 
        increasing_score = 1 * difficulty
        self.dirnx = 0
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        if score >= highscore:
            highscore = score
            score = 0
        if score < highscore:
            score = 0

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
        #Added these to allow for diagonal movement in terms of addition of cubes when the snake eats the snack

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy  

    # This refers to being able to draw the snake and specifically to draw the head with eyes and the rest without
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def rand(x_or_y): # added to create random X and Y values in the reset
        global difficulty
        if x_or_y == 'X':
            randX = random.randrange((one_row)*difficulty,rows-((one_row)*difficulty))
            return randX
        if x_or_y == 'Y':
            randY = random.randrange(rows * ratio_header_to_screen, rows-((one_row)*difficulty))
            return randY 

def redrawWindow(surface):
    global s, snack, score, increasing_score, positions_snack, highscore, difficulty 
    border = width // rows # ratio'd to number of rows
    surface.fill(pastel_green, rect=[border*difficulty,width * ratio_header_to_screen, width - border*difficulty, width - width * ratio_header_to_screen]) # Drawing playing space
    surface.fill(emerald,rect=[0,0, width, width * ratio_header_to_screen]) # Drawing header
    surface.fill(emerald,rect=[0,width-border*difficulty, width, border*difficulty]) # Drawing 
    surface.fill(emerald,rect=[0,width * ratio_header_to_screen, border*difficulty, width - width * ratio_header_to_screen])
    surface.fill(emerald,rect=[width-border*difficulty,width * ratio_header_to_screen, border*difficulty, width - width * ratio_header_to_screen]) # Bottom barrier New Boston
    centered_txt2_screen('Score '+str(score)+'    '+'Highscore '+str(highscore), white, 2, size=medfont)
    s.draw(surface)
    surface.blit(img_apple, (rows * positions_snack[0],rows * positions_snack[1]))
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

smallfont = pygame.font.Font('Fonts/OpenSans-Light.ttf', 25)
medfont = pygame.font.Font("Fonts/Roboto-ThinItalic.ttf", 50)
largefont = pygame.font.Font("Fonts/PlayfairDisplaySC-BoldItalic.otf", 75)
bubblefont = pygame.font.Font("Fonts/Bubblegum.ttf", 75)


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

def centered_txt2_screen(msg,color, row_nr=rows//2,size=smallfont): 
    textSurf, textRect = text_objects(msg, color, size)  #textSurf is just like pygame surf, textRect
    textRect.center = (width // 2), (row_nr * (width // rows)) # aimed to get the message placed on screen
    win.blit(textSurf, textRect)


def main():
    global width, s, snack, surface, score, positions_snack, highscore, difficulty
    score = 0 
    increasing_score = 1 * difficulty
    s = snake(purple, (rand('X'),rand('Y'))) 
    positions_snack = (randomSnack(rows,s))
    snack = cube(positions_snack,color=red)
    gameOn = True
    gameOver = False
    clock = pygame.time.Clock()


    while gameOn:
        FPS = 20 + 10*(difficulty) # Sets 'pace' of game through FPS and by level of difficulty selected
        pygame.time.delay(0)       # 0 to allow for quick response in changing direction
        clock.tick(FPS)           
        s.move()                   # Allows for mvovement of snake
        if gameOver == True: # What happens when game Over
            s.reset((100,100))
            centered_txt2_screen("Game Over!", red, 10, size = bubblefont)
            centered_txt2_screen("Try again?              or too much 'bite'?", white, 15, size = medfont)
            centered_txt2_screen("P = Play Again!         T = Till Later!", black, 25, size = medfont)
            pygame.display.update()
            for event in pygame.event.get():  # Options of game Over screen
                if event.type == pygame.QUIT: 
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
        
        #To allow for the snake to get the snack from all four points of the cube:

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
            increasing_score = 1 * difficulty
            gameOver = True
            continue
            
        elif s.body[0].pos[0] >= rows - (one_row) * difficulty: 
            increasing_score = 1 * difficulty
            gameOver = True
            continue

        elif s.body[0].pos[1] <= rows * ratio_header_to_screen - (one_row): 
            increasing_score = 1 * difficulty
            gameOver = True
            continue
            
        elif s.body[0].pos[1] >= rows - (one_row)*difficulty:
            gameOver = True
            continue
        
        for g in range(len(s.body)):
            if s.body[g].pos in list(map(lambda z:z.pos,s.body[g+1:])):
                if score >= highscore:
                    highscore = score
                main()
                s.reset((10,10))
                break
            continue

        redrawWindow(win)
start_screen()   # ensure starting with the start screen

