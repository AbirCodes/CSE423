from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random


left = 0
right =  0
pause = False
gameOver = False
score = 0
special_counter=0

a,b = 245,45 #shooter
life = 3
bullet = []
target = []


def midpointCircle(radius, x0, y0):
    d = 1 - radius 
    x = 0
    y = radius
    circlePoints(x, y, x0, y0)
    while x < y:
        x += 1
        if d < 0:
            d += 2*x + 3
        else:
            d += 2*x - 2*y + 5
            y = y - 1
        circlePoints(x, y, x0, y0)
def circlePoints(x, y, x0, y0):
    zones=[(x,y),(y,x),(y,-x),(x,-y),(-x,-y),(-y,-x),(-y,x),(-x,y)]
    for i in range(8):
            glPointSize(1.3)
            glBegin(GL_POINTS)
            glVertex2f(zones[i][0]+ x0, zones[i][1] + y0)
            glEnd()
def drawline(x0, y0, x1, y1):
    zone = zonefinder(x0, y0, x1, y1)
    x0, y0 = convert_zero(zone, x0, y0)
    x1, y1 = convert_zero(zone, x1, y1)
    dx = x1 - x0
    dy = y1 - y0
    dinit = 2 * dy - dx
    dne = 2 * (dy - dx)
    de = 2 * dy

    while x0 < x1:
        a, b = convert_Original(zone, x0, y0)
        glPointSize(2)
        glBegin(GL_POINTS)
        glVertex2f(a,b)
        glEnd()
        if dinit >= 0:
          dinit = dinit + dne
          x0 += 1
          y0 += 1
        else:
            dinit = dinit + de
            x0 += 1

def zonefinder(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) >= abs(dy): #For Zone 0, 3, 4 & 7
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
        
    else: #For zone 1, 2, 5 & 6
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def convert_zero(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
   
def convert_Original(zone, x, y):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y

def shooter(a,b):
    
    global left,right,gameOver,score
    glColor3f(1.0,1.0,0.0)
    if gameOver == True:
        print(f'Game Over! Score: {score}')
        glColor3f(1.0,0.0,0.0)
    drawline(a-left+right,b,a-left+right-5,b-10)
    drawline(a-left+right,b,a-left+right+5,b-10)
    drawline(a-left+right-5,b-10,a-left+right+5,b-10)
    drawline(a-left+right-5,b-10,a-left+right-5,b-25)
    drawline(a-left+right-5,b-25,a-left+right-10,b-30)
    drawline(a-left+right-10,b-30,a-left+right-5,b-30)
    drawline(a-left+right-5,b-25,a-left+right-5,b-30)
    drawline(a-left+right-5,b-30,a-left+right+5,b-30)
    
    drawline(a-left+right+5,b-25,a-left+right+5,b-30)
    drawline(a-left+right+5,b-30,a-left+right+10,b-30)
    drawline(a-left+right+5,b-25,a-left+right+10,b-30)
    drawline(a-left+right+5,b-10,a-left+right+5,b-30)


def fire_b():
    global a,b,left,right,bullet
    if pause == False:        
        p = a-left+right
        q = b
        bullet.append([p,q])

def enemy():
        global special_counter
        if len(target) == 0:
            if special_counter==5:
                x,y = random.randint(30,470),430 
                target.append([random.randint(20,30),x,y,(0,1.0,0.0),True,True])       
            
            else:
                x,y = random.randint(30,470),430 
                target.append([random.randint(20,30),x,y,(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
,False,False])


def special_enemy(i):
                global special_counter,pause
                if pause == False:
                    if i[5]:
                            i[0] += 0.5
                            if i[0] >= 30: 
                                i[5] = False
                    else:
                            i[0] -= 0.5 #
                            if i[0] <= 0:
                                i[5] = True             
                    special_counter=0
                        

def exit(): #cross
    glColor3f(1.0,0.0,0.0)
    drawline(450,490,480,460)
    drawline(450,460,480,490)

def restart(): #arrow
    glColor3f(0.0, 1.0, 0.0)
    drawline(5,475,40,475)
    drawline(5,475,20,460)
    drawline(5,475,20,490)

def pauser(): #lines
    glColor3f(0.75, 0.25, 0.5)
    if not pause:
        drawline(255,490,255,460)
        drawline(265,490,265,460)
    else:
        glColor3f(1.0,1.0,0.0)
        drawline(255,495,255,455)
        drawline(255,495,275,475)
        drawline(255,455,275,475)

def restarter():
    if not pause:
        global a,b,score,gameOver,left,right,life,bullet,target,special_counter
        a,b,left,right,score,special_counter,gameOver,life,target,bullet= 245,25,0,0,0,0,False,3,[],[]

def keyboardListener(key, x, y):
    if key == b' ':
        fire_b()
        
def specialKeyListener(key,g,f):
    global left, right, a
    if pause == False:
        if key == GLUT_KEY_LEFT:
            if a - left + right > 20:
                left += 4
        elif key == GLUT_KEY_RIGHT:
            if a + 100 - left + right <= 570:
                right += 4
    glutPostRedisplay()

def mouseListener(button, state, p, q):
    global pause
    if button == GLUT_LEFT_BUTTON and (state == GLUT_DOWN):
        if 5<=p<=40 and 10<=q<=40:#restart button
            restarter()
        if not gameOver and 245<=p<=280 and 5<=q<=45:#pause button 
            pause = not pause
        if 450<=p<=480 and 10<=q<=40:#exit button
            glutLeaveMainLoop()

def collison():
    global a,b,left,right,life,gameOver,bullet,target,score,special_counter
    for i in target:
        if i[2] <= 25:
            target.remove(i)
            life -= 1
            print(f"Missed Target, lives remaining {life}")
        if life == 0:
            gameOver = True

        d = (((a-left+right)-i[1])**2 + (b-i[2])**2)**.5
        if d == (14+i[0]) or  d < (14+i[0]):
            gameOver = True
            print('Spaceship Crashed')
        else:
            continue
    
    for k in target:
        for j in bullet:
            d = ((j[0]-k[1])**2 + (j[1]-k[2])**2)**.5
            if d <= (k[0]+9):
                target.remove(k)
                bullet.remove(j)
                if k[4]==True:
                  print('Congrats! you have hit the bonus')
                  score+=5
                else:
                    score+=1
                special_counter+=1
                print(special_counter)
                print(f"SCORE : {score}")
            else:
                continue

def animate():
    global pause,bullet,gameOver,target,life,special_counter

    #for bullet
    if not gameOver:
        for i in bullet:
            glColor3f(1.0,1.0,0.0)
            midpointCircle(9,i[0],i[1])
            if pause == False:
                i[1] += 1
                if i[1] == 450:
                    life -= 1
                    print(f'missed a shot. Life remainig {life}')
                    bullet.remove(i)
        #for target
        for i in target:
            if i[4] or special_counter>=5:
                special_enemy(i)
            glColor3f(*(i[3]))
            midpointCircle(i[0],i[1],i[2])
            if pause == False:
                    i[2] -= 0.22
                    if i[2] == 300:
                        target.append([random.randint(20,50),random.randint(40,460),430,(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
,False,False])
                    if i[2] == 0:
                        target.remove(i)
    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
def showScreen():
    if gameOver:
        return
    global a,b
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    collison()
    animate()
    shooter(a,b)
    enemy()
    exit()
    pauser()
    restart()
    
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Shooter")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()