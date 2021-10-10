import pygame
import random
import math
import cv2 as cv
import numpy as np
import os
import HSV_Detector as HSV
from pygame import mixer

#Window dimensions
w=560
h=480

#Dimensions of icons
imgSize=24

cap = cv.VideoCapture(0)

#The variables for the dynamic stylus
num=1

i=1

x_=0
y_=0

cx=0
cy=0
quadY=0
quadX=0

slope1=0
slope=0

angle=0

#HSV
color=HSV.hsv_Detector()

#Initialize pygame
pygame.init()

#Positioning the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (640,100)
#Create the game screen
screen=pygame.display.set_mode((w, h))

#Title and Icon of the Window
pygame.display.set_caption("Snake")
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

#Player
headX=0
headY=0
snake=[]
playerImg=[]

speed=3

#Length of the snake
length=5

for i in range(length):
    if i==0:
        playerImg.append(pygame.image.load('head.png'))
    else:
        playerImg.append(pygame.image.load('body.png'))
    #Coordinates of player
    snake=[[50,h/2-200],[50-speed,h/2-200],[50-2*speed,h/2-200],
            [50-3*speed,h/2-200],[50-4*speed,h/2-200]]
    headX=50
    headY=h/2-200

state='first'
change='first'

#Fruit
fruitImg=pygame.image.load('fruit.png')
#Respawn random coordinates
fruitX=random.randint(0,w-imgSize)
fruitY=random.randint(0,h-imgSize)

#Hurdles
wallImg=pygame.image.load('wall.png')

design1=[[100,100],[100,124],[100,148],[100,172],[100,316],[100,340],[100,364],[100,388],
        [460,100],[460,124],[460,148],[460,172],[460,316],[460,340],[460,364],[460,388],
        [124,100],[148,100],[172,100],[196,100],[364,100],[388,100],[412,100],[436,100],
        [124,388],[148,388],[172,388],[196,388],[364,388],[388,388],[412,388],[436,388]]

design2=[[w/2,h/2-144],[w/2,h/2-120],[w/2,h/2-96],[w/2,h/2-72],[w/2,h/2-48],[w/2,h/2-24],[w/2,h/2],[w/2,h/2+24],
        [w/2,h/2+48],[w/2,h/2+72],[w/2,h/2+96],[w/2,h/2+120],[w/2,h/2+144],
        [w/2-192,h/2],[w/2-168,h/2],[w/2-144,h/2],[w/2-120,h/2],[w/2-96,h/2],[w/2-72,h/2],[w/2-48,h/2],[w/2-24,h/2],[w/2+24,h/2],
        [w/2+48,h/2],[w/2+72,h/2],[w/2+96,h/2],[w/2+120,h/2],[w/2+144,h/2],[w/2+168,h/2],[w/2+192,h/2]]

design3=[[192,0],[192,24],[192,48],[192,72],[192,96],[192,120],[192,144],
        [536,144],[512,144],[488,144],[464,144],[440,144],[416,144],[392,144],[368,144],
        [368,456],[368,432],[368,408],[368,384],[368,360],[368,336],[368,312],
        [192,312],[168,312],[144,312],[120,312],[96,312],[72,312],[48,312],[24,312],[0,312]]
# For design 3, state should be 'down'

design4=[[200,100],[200,124],[200,148],[200,172],[200,196],[200,220],
        [200,244],[200,268],[200,292],[200,316],[200,340],[200,364],
        [360,100],[360,124],[360,148],[360,172],[360,196],[360,220],
        [360,244],[360,268],[360,292],[360,316],[360,340],[360,364]]

design5=[[104,100],[128,100],[152,100],[176,100],[200,100],[224,100],[248,100],[272,100],
        [296,100],[320,100],[344,100],[368,100],[392,100],[416,100],[440,100],
        [104,356],[128,356],[152,356],[176,356],[200,356],[224,356],[248,356],[272,356],
        [296,356],[320,356],[344,356],[368,356],[392,356],[416,356],[440,356]]

design6=[[150,100],[174,100],[198,100],[150,124],[174,124],[198,124],[150,148],[174,148],[198,148],
        [150,356],[174,356],[198,356],[150,332],[174,332],[198,332],[150,308],[174,308],[198,308],
        [384,100],[360,100],[336,100],[384,124],[360,124],[336,124],[384,148],[360,148],[336,148],
        [384,356],[360,356],[336,356],[384,332],[360,332],[336,332],[384,308],[360,308],[336,308],
        [253,217],[277,217],[253,241],[277,241]]

design7=[[200,102],[200,126],[200,150],[200,174],[176,174],[152,174],[128,174],[104,174],
        [176,260],[152,260],[128,260],[104,260],[200,260],[200,284],[200,308],[200,332],
        [350,102],[350,126],[350,150],[350,174],[374,174],[398,174],[422,174],[446,174],
        [374,260],[398,260],[422,260],[446,260],[350,260],[350,284],[350,308],[350,332]]

design8=[[224,78],[200,102],[176,126],[152,150],[128,174],
        [128,284],[152,308],[176,332],[200,356],[224,380],
        [326,78],[350,102],[374,126],[398,150],[422,174],
        [422,284],[398,308],[374,332],[350,356],[326,380]]

design=[design1,design2,design3,design4,design5,design6,design7,design8]
designNum=random.randint(0,7)

if designNum==2:
    state='down'

wall=design[designNum]

#Wall length
wallLength=len(wall)

#Wall Collision
Wallcollision=False

#To avoid Fruit spawning on the walls
FruitCollision=False

#Score
score_value=0

#Coordinate of Scorecard
textX=10
textY=10

#BodyCollision
BodyCrash=False

#Define font
font=pygame.font.Font('freesansbold.ttf',16)

#Game Over
over_font=pygame.font.Font('freesansbold.ttf',64)
final_score=pygame.font.Font('freesansbold.ttf',32)

def show_score(x,y):
    score=font.render("Score: "+str(score_value),True,(255,255,255)) 
    screen.blit(score, (x, y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,0,0))
    score_text=final_score.render("Your Score is "+str(score_value),True,(0,255,0))
    screen.blit(over_text, (w/2-200,h/2-50)) #Middle Of the screen
    screen.blit(score_text, (w/2-120,(h+32)/2))

def player(position,j):
    screen.blit(playerImg[j], (position[0], position[1]))
    #Drawing an image of player onto our screen/surface

def fruit(x,y):
    screen.blit(fruitImg, (x, y))
    #Drawing an image of fruit onto our screen/surface

def Wall(position):
    screen.blit(wallImg, (position[0], position[1]))
    #Drawing an image of wall onto our screen/surface

def isCollision(fruitX,fruitY,playerX,playerY,dist):
    distance=math.sqrt((math.pow(fruitX-playerX,2))+(math.pow(fruitY-playerY,2))) #Algebraic Distance
    if distance <dist:
        return True
    else:
        return False

#Initializing the Game Loop
running=True
while running:

    #Background
    screen.fill((0,80,0))
    #----------------------------------------------------------------------------------------------------------

    # Take each frame
    ret, frame = cap.read()
    frame = cv.resize(frame, (w,h))
    frame = cv.flip(frame, 1)

    #Removing noise of the frame
    filtered_frame = cv.GaussianBlur(frame,(11,11),0)
    
    # Convert BGR to HSV
    hsv = cv.cvtColor(filtered_frame, cv.COLOR_BGR2HSV)

    #define range of color in HSV
    lower = np.array([color[0]-20,color[1]-50,color[2]-50])
    upper = np.array([color[0]+10,255,255])

    #Threshold the HSV image to get only the color
    mask = cv.inRange(hsv, lower, upper)

    kernel = np.ones((7,7),np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

    #Contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    if len(contours)!=0:

        cnt = contours[0]
        M = cv.moments(cnt)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        center = (cx,cy)
        cv.circle(frame,center,3,(0,0,255),-1)

        if i!=1:
            quadY=cy-y_
            quadX=cx-x_

            if abs(cy-y_)<40 and abs(cx-x_)<40: #Setting a threshold
                change=change
            elif cx-x_==0 and cy-y_>0:
                change='+infinite'
            elif cx-x_==0 and cy-y_<0:
                change='-infinite'
            else:
                slope1= (cy-y_)/(cx-x_)
                if slope1>0:
                    if quadY>=0 and quadX>=0:
                        change='first'
                    if quadY<=0 and quadX<=0:
                        change='third'
                if slope1<0:
                    if quadY>=0 and quadX<=0:
                        change='second'
                    if quadY<=0 and quadX>=0:
                        change='fourth'
                if slope1==0:
                    change=change

                (x_,y_)=center
        else:
            (x_,y_)=center
            i=i+1
    
    else:
        i=1
        x_=0
        y_=0

    cv.imshow('frame',frame)
    cv.moveWindow('frame',640-w-10,70)
    cv.waitKey(1)
#-----------------------------------------------------------------------------------------------------
    #If Snake Crashes into the Wall
    for j in range(wallLength):
        wallCrash=isCollision(wall[j][0],wall[j][1],headX,headY,20)
        if wallCrash==True:
            Wallcollision=True
            break
    
    #To prevent Fruit from spawning in the wall
    for j in range(wallLength):
        FruitCrash=isCollision(wall[j][0],wall[j][1],fruitX,fruitY,20)
        if FruitCrash==True:
            FruitCollision=True
            break
    
    while(FruitCollision):
        FruitCollision=False
        fruitX=random.randint(0,w-imgSize)
        fruitY=random.randint(0,h-imgSize)
        for j in range(wallLength):
            FruitCrash=isCollision(wall[j][0],wall[j][1],fruitX,fruitY,20)
            if FruitCrash==True:
                FruitCollision=True
                break
    
    #If snake bites itself
    for j in range(5,length):
        bite=isCollision(snake[j][0],snake[j][1],headX,headY,2)
        if bite:
            BodyCrash=True
            break

    #Game Over condition
    if headX<0 or headX>w-imgSize or headY<0 or headY>h-imgSize or BodyCrash or Wallcollision: 

        speed=0
        #Display Final Position of everything
        for j in range(length):
            player(snake[j],j)
        for k in range(wallLength):
            Wall(wall[k])
        
        fruit(fruitX,fruitY)

        #Collision Sound played once
        if num==1:
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            num+=1
        
        #Display the game over text
        game_over_text()

        for event in pygame.event.get():
            if event.type==pygame.QUIT: #Close Button
                running=False
    else:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: #Close Button
                running=False
        
        fruit(fruitX,fruitY)
        
        if slope1*slope!=-1:
            angle= abs((slope1-slope)/(1+slope1*slope))
        else:
            angle=100
        
        #To prevent going in the opposite direction
        if state=='first' and change=='third' and angle<1.5:
            state=state
            slope=slope
        elif state=='second' and change=='fourth' and angle<1.5:
            state=state
            slope=slope
        elif state=='third' and change=='first' and angle<1.5:
            state=state
            slope=slope
        elif state=='fourth' and change=='second' and angle<1.5:
            state=state
            slope=slope
        elif state=='infinte' and change=='-infinite':
            state=state
        elif state=='-infinte' and change=='infinite':
            state=state
        else:
            state=change
            slope=slope1

        #Direction of Dynamic Motion
        if state=='first':
            headX+=speed*math.cos(math.atan(slope))
            headY+=speed*math.sin(math.atan(slope))
        if state=='fourth':
            headX+=speed*math.cos(math.atan(slope))
            headY+=speed*math.sin(math.atan(slope))
        if state=='second':
            headX-=speed*math.cos(math.atan(slope))
            headY-=speed*math.sin(math.atan(slope))
        if state=='third':
            headX-=speed*math.cos(math.atan(slope))
            headY-=speed*math.sin(math.atan(slope))
        if state=='+infinite':
            headY+=speed
            headX=headX
        if state=='-infinite':
            headY-=speed
            headX=headX
        
        #Movement of the snake
        snake.insert(0,[headX,headY])

        #If Collision occurs
        collision=isCollision(fruitX,fruitY,headX,headY,16)
        if collision:
            #Score should increase
            score_value+=10
            #Speed if score is a multiple of 50
            if score_value%50==0 and score_value!=0:
                speed+=0.5
            #fruit Respawns
            fruit_sound=mixer.Sound("fruit.wav")
            fruit_sound.play()
            fruitX=random.randint(0,w-imgSize)
            fruitY=random.randint(0,h-imgSize)
            #Length of the snake should increase
            playerImg.append(pygame.image.load('body.png'))
            length+=1
        else:
            #Length should be constant
            snake.pop()

        for j in range(length):
            player(snake[j],j)
            
        for k in range(wallLength):
            Wall(wall[k])
        
        show_score(textX,textY)     

    pygame.display.update()
#-------------------------------------------------------------------------------------------------------
cap.release()
cv.destroyAllWindows()