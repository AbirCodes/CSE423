
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math
from threading import Timer

W_Width, W_Height = 500,500
space=False
blink= False
speed = 0.05
all_points=[]




def amazing_box():
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2d(-180,180)
    glVertex2d(180,180)

    glVertex2d(180,180)
    glVertex2d(180,-180)
    glVertex2d(180,-180)
    glVertex2d(-180,-180)

    glVertex2d(-180,-180)
    glVertex2d(-180,180)
    glEnd()

def generate_point():
    global all_points
    for x,y,color,direct in all_points:
        glPointSize(10)
        if blink:
            glColor3f(0,0,0)
        else:
           glColor3f(color[0],color[1],color[2])
        glBegin(GL_POINTS)
        glVertex2d(x,y)
        glEnd()

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b
def keyboardListener(key, x, y):

    global space
    if key==b' ':
        space = not space
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
   
    if key==GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key== GLUT_KEY_DOWN:		#// up arrow key
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()

def mouseListener(button, state, x, y):	
    global all_points,blink,space
    if space == False:
        if button==GLUT_RIGHT_BUTTON:
            if(state == GLUT_DOWN): 
                x,y=convert_coordinate(x,y)
                if x > -180 and x<180 and y>-180 and y<180:
                    direct=random.choice([(-1, 1), (-1, -1), (1,1), (1, -1)])
                    color=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
                    all_points.append((x,y,color,direct))
        if button == GLUT_LEFT_BUTTON:
            if(state == GLUT_DOWN):
                blink = not blink
            

            
def blinking_points(old_colors):
    global blink
    if blink:
     blink= not blink

    glutPostRedisplay()
    glutTimerFunc(100,blinking_points,0)#recalls the function after dedicated time(ms)



def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,1);	#//color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    amazing_box()

    generate_point()





    glutSwapBuffers()


def animate():
    glutPostRedisplay()
    global all_points,speed,space,blink,old_colors
    if space == False:
        old_colors=[]
        for index,(x,y,color,direct) in enumerate(all_points):
            direct_x,direct_y=direct
            old_colors.append(color)
            x+=(direct_x)*speed
            y+=(direct_y)*speed
            if x >= 180 or x <= -180:
                direct_x*=-1
            elif y >= 180 or y <= -180:
                direct_y*=-1
            all_points[index]=(x,y,color,(direct_x,direct_y))
        if blink:
            for index,(x,y,color,direct) in enumerate(all_points):
                all_points[index]=(x,y,old_colors[index],direct)
        

    
        

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)
  


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 

wind = glutCreateWindow(b"Task 2")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
glutTimerFunc(1000,blinking_points,0)
glutKeyboardFunc(keyboardListener) #alphaneumeric key pressed
glutSpecialFunc(specialKeyListener) # other than alphaneumeric values
glutMouseFunc(mouseListener) #mouse clicking

glutMainLoop()		
