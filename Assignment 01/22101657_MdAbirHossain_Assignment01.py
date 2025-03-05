#task 01

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 500,500
angle=0.05
background_color=[0.0,0.0,0.0]


all_raindrops=[]

for i in range(100):
    x=random.uniform(-200,200)
    y=random.uniform(-200,200)
    all_raindrops.append((x,y))

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_raindrops(s):
    for x,y in s:
        glLineWidth(2) 
        glBegin(GL_LINES)
        glVertex2f(x,y) 
        glVertex2f(x,y+10) 
        glEnd()

def drawHouse():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0,0,255)
    #roof 
    glVertex2f(0,200)
    glVertex2f(200,50)
    glVertex2f(200,50)
    glVertex2f(-200,50)
    glVertex2f(-200,50)
    glVertex2f(0,200)

    #rectanle
    glVertex2f(-150,50)
    glVertex2f(-150,-100)

    glVertex2f(-150,-100)
    glVertex2f(150,-100)

    glVertex2f(150,-100)
    glVertex2f(150,50)

    #door
    glColor3f(0,1,0)

    glVertex2f(-100,-100)
    glVertex2f(-100,0)
    
    glVertex2f(-100,0)
    glVertex2f(-50,0)

    glVertex2f(-50,0)
    glVertex2f(-50,-100)

    #window
    glColor3f(255,0,255)

    glVertex2f(80,0)
    glVertex2f(130,0)

    glVertex2f(130,0)
    glVertex2f(130,-50)

    glVertex2f(130,-50)
    glVertex2f(80,-50)

    glVertex2f(80,-50)
    glVertex2f(80,0)

    glVertex2f(105,0)
    glVertex2f(105,-50)

    glVertex2f(80,-25)
    glVertex2f(130,-25)
    glEnd()
    #doornob

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(-60,-45)
    glEnd()




def specialKeyListener(key, x, y):
    global angle,background_color
    if key==GLUT_KEY_RIGHT:
        angle+=0.5
        print("Tilting")
        
    if key==GLUT_KEY_LEFT:
         angle-=0.5
         print("Tilting ")
        

    if key==GLUT_KEY_PAGE_UP:
        background_color[0]+=0.1
        background_color[1]+=0.1
        background_color[2]+=0.1
        print(background_color)
       
    if key==GLUT_KEY_PAGE_DOWN:
        background_color[0]-=0.1
        background_color[1]-=0.1
        background_color[2]-=0.1
        print(background_color)



    glutPostRedisplay()

def display():
    global all_raindrops,background_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(background_color[0],background_color[1],background_color[2],1);	
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
 
    glLoadIdentity()

    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_raindrops(all_raindrops)
    drawHouse()

    glutSwapBuffers()


def animate():
    global all_raindrops,angle,W_Height
    for i in range(len(all_raindrops)):
        x,y = all_raindrops[i]
        x += angle
        y -=1
        if y < 0:
            y = W_Height
        elif y < 50:
            x = random.uniform(-200,200)
            y = random.uniform(-200,200)
           
        all_raindrops[i]=(x,y)
    glutPostRedisplay()
    draw_raindrops(all_raindrops)

def init():
  
    glClearColor(0,0,0,0)
  
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(104,	1,	1,	1000.0)
   


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutSpecialFunc(specialKeyListener) # other than alphaneumeric values

glutMainLoop()		#The main loop of OpenGL


#task 2

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time
# import math
# from threading import Timer

# W_Width, W_Height = 500,500
# space=False
# blink= False
# speed = 0.05
# all_points=[]




# def amazing_box():
#     glColor3f(0.0, 1.0, 1.0)
#     glBegin(GL_LINES)
#     glVertex2d(-180,180)
#     glVertex2d(180,180)

#     glVertex2d(180,180)
#     glVertex2d(180,-180)
#     glVertex2d(180,-180)
#     glVertex2d(-180,-180)

#     glVertex2d(-180,-180)
#     glVertex2d(-180,180)
#     glEnd()

# def generate_point():
#     global all_points
#     for x,y,color,direct in all_points:
#         glPointSize(10)
#         if blink:
#             glColor3f(0,0,0)
#         else:
#            glColor3f(color[0],color[1],color[2])
#         glBegin(GL_POINTS)
#         glVertex2d(x,y)
#         glEnd()

# def convert_coordinate(x,y):
#     global W_Width, W_Height
#     a = x - (W_Width/2)
#     b = (W_Height/2) - y 
#     return a,b
# def keyboardListener(key, x, y):

#     global space
#     if key==b' ':
#         space = not space
#     glutPostRedisplay()

# def specialKeyListener(key, x, y):
#     global speed
   
#     if key==GLUT_KEY_UP:
#         speed *= 2
#         print("Speed Increased")
#     if key== GLUT_KEY_DOWN:		#// up arrow key
#         speed /= 2
#         print("Speed Decreased")
#     glutPostRedisplay()

# def mouseListener(button, state, x, y):	
#     global all_points,blink,space
#     if space == False:
#         if button==GLUT_RIGHT_BUTTON:
#             if(state == GLUT_DOWN): 
#                 x,y=convert_coordinate(x,y)
#                 if x > -180 and x<180 and y>-180 and y<180:
#                     direct=random.choice([(-1, 1), (-1, -1), (1,1), (1, -1)])
#                     color=[random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
#                     all_points.append((x,y,color,direct))
#         if button == GLUT_LEFT_BUTTON:
#             if(state == GLUT_DOWN):
#                 blink = not blink
            

            
# def blinking_points(old_colors):
#     global blink
#     if blink:
#      blink= not blink

#     glutPostRedisplay()
#     glutTimerFunc(100,blinking_points,0)#recalls the function after dedicated time(ms)



# def display():
    
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0,0,0,1);	#//color
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
    
#     gluLookAt(0,0,200,	0,0,0,	0,1,0)
#     glMatrixMode(GL_MODELVIEW)

#     amazing_box()

#     generate_point()





#     glutSwapBuffers()


# def animate():
#     glutPostRedisplay()
#     global all_points,speed,space,blink,old_colors
#     if space == False:
#         old_colors=[]
#         for index,(x,y,color,direct) in enumerate(all_points):
#             direct_x,direct_y=direct
#             old_colors.append(color)
#             x+=(direct_x)*speed
#             y+=(direct_y)*speed
#             if x >= 180 or x <= -180:
#                 direct_x*=-1
#             elif y >= 180 or y <= -180:
#                 direct_y*=-1
#             all_points[index]=(x,y,color,(direct_x,direct_y))
#         if blink:
#             for index,(x,y,color,direct) in enumerate(all_points):
#                 all_points[index]=(x,y,old_colors[index],direct)
        

    
        

# def init():
#     glClearColor(0,0,0,0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(104,	1,	1,	1000.0)
  


# glutInit()
# glutInitWindowSize(W_Width, W_Height)
# glutInitWindowPosition(0, 0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 

# wind = glutCreateWindow(b"Task 2")
# init()

# glutDisplayFunc(display)	#display callback function
# glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
# glutTimerFunc(1000,blinking_points,0)
# glutKeyboardFunc(keyboardListener) #alphaneumeric key pressed
# glutSpecialFunc(specialKeyListener) # other than alphaneumeric values
# glutMouseFunc(mouseListener) #mouse clicking

# glutMainLoop()		
