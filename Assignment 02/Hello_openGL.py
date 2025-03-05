from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(0.0, 1.0, 1.0) #konokichur color set (RGB)
    #call the draw methods here
    #point 1
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(250,250)
    glEnd()

     #point 2
    glPointSize(50)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0) #RGB color set
    glVertex2f(450, 250)
    glEnd()

    #line 1
    glLineWidth(10)
    glBegin(GL_LINES)
    glVertex2f(300,300)
    glVertex2f(400,300)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)
    # line 2
    glLineWidth(10)
    glBegin(GL_LINES)
    glVertex2f(375, 400)
    glVertex2f(375, 100)
    glEnd()


    #triangle (have to give points anti clockwise
    glColor3f(0.0, 0.0, 1.0)
    glLineWidth(10)
    glBegin(GL_TRIANGLES)
    glVertex2f(75, 300)
    glVertex2f(50, 200)
    glVertex2f(100, 200)

    glEnd()

    #draw_points(250, 250)
    glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()