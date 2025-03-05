from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

W_WIDTH, W_HEIGHT = 500, 790
firing_ball = [] 
score = 0
missed_fire_shot = 0
pause = False
gameover = 0
bonus_ball = None  
bonus_ball_timer = 0 
expand = True  

class Falling_balls:  # balls from above are randomly being generated
    def __init__(self):
        self.x = random.randint(-220, 220) 
        self.y = 330 
        self.r = random.randint(20, 25)
        self.color = [1, 1, 0]

class Bonus_ball(Falling_balls):    ##subclass of falling_balls class
    def __init__(self):
        super().__init__()
        self.r = random.randint(15, 20)
        self.color = [0, 1, 0]  

class Catcher: # THE Spaceship
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

def plot_point(x, y):  #visually representing every ball points, spaceship points
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def Convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def from_zone0(x, y, zone):   #from zone 0 to its original zone
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):                  # selecting zones
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = Convert_to_zone0(x1, y1, zone)
    x2, y2 = Convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrEast = 2 * dy
    incrNorthEast = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = from_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrEast
            x += 1
        else:
            d += incrNorthEast
            x += 1
            y += 1
        x0, y0 = from_zone0(x, y, zone)
        plot_point(x0, y0)

def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:   
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

bubble = [Falling_balls(),Falling_balls(), Falling_balls(), Falling_balls(), Falling_balls(), Falling_balls()] # Initializes six Falling_balls objects
bubble.sort(key=lambda b: b.x) # sorts them by their x coordinate.
catcher = Catcher()

def draw_firing_ball(): #firing_ball draw ekhane hoi
    global firing_ball #empty list, firing_ball list theke use kore
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in firing_ball:
        midpointcircle(8, i[0], i[1]) # 
def draw_bubble(): # midpointcircle use kore regular and unique circle draw
    global bubble, bonus_ball 
    glPointSize(2)

    for i in range(len(bubble)): 
        if i == 0: # The first bubble (index 0) is drawn
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2]) #sets the RGB color
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y) #circle draw
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (   #
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)): #
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)


    if bonus_ball:
        glColor3f(bonus_ball.color[0], bonus_ball.color[1], bonus_ball.color[2])
        midpointcircle(bonus_ball.r, bonus_ball.x, bonus_ball.y)
def draw_ui():
    global catcher
    glPointSize(2)
    base_x = catcher.x  # position of the catcher
    base_y = -350  

    glColor3f(1, 1, 0)  
    # Draw triangular tip (outline)
    glBegin(GL_LINE_LOOP)
    glVertex2f(base_x, base_y + 70)  # Top point
    glVertex2f(base_x - 20, base_y + 40)  # Bottom-left point
    glVertex2f(base_x + 20, base_y + 40)  # Bottom-right point
    glEnd()

    # Draw rectangular body (outline)
    glBegin(GL_LINE_LOOP)
    glVertex2f(base_x - 10, base_y + 40)  # Top-left
    glVertex2f(base_x + 10, base_y + 40)  # Top-right
    glVertex2f(base_x + 10, base_y - 20)  # Bottom-right
    glVertex2f(base_x - 10, base_y - 20)  # Bottom-left
    glEnd()

    glBegin(GL_LINE_LOOP)  # Draw fins (outline)
    glVertex2f(base_x - 10, base_y - 10)  # Top-left of fin
    glVertex2f(base_x - 20, base_y - 20)  # Bottom-left of fin
    glVertex2f(base_x - 10, base_y - 20)  # bottom point of fin
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex2f(base_x + 10, base_y - 10)  # Top-right of fin
    glVertex2f(base_x + 20, base_y - 20)  # Bottom-right of fin
    glVertex2f(base_x + 10, base_y - 20)  # Inner point of fin
    glEnd()

    glBegin(GL_LINE_LOOP)  # Left pipe
    glVertex2f(base_x - 15 , base_y - 27 )  
    glVertex2f(base_x - 15, base_y - 40 )
    glVertex2f(base_x - 10, base_y - 40 )
    glVertex2f(base_x - 10, base_y - 27 )
    glEnd()

    glBegin(GL_LINE_LOOP)    # Center pipe
    glVertex2f(base_x-5, base_y - 27 ) 
    glVertex2f(base_x-5, base_y - 40 )
    glVertex2f(base_x, base_y - 40 )
    glVertex2f(base_x, base_y - 27 )
    glEnd()

    glBegin(GL_LINE_LOOP)  # Right pipe
    glVertex2f(base_x + 5, base_y - 27 ) 
    glVertex2f(base_x + 5, base_y - 40 )
    glVertex2f(base_x + 10, base_y - 40 )
    glVertex2f(base_x + 10, base_y - 27 )
    glEnd()

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if pause: # play icon
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else: # pauseicon
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    # Right Cross Button
    glPointSize(4)
    glColor3f(0.9, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)
    
    render_text(-240, 310, f"Score: {score}", color=(1, 1, 1))    
    render_text(-240, 290, f"Missfires: {missed_fire_shot }", color=(1, 0, 0))  
    render_text(-240, 270, f"Missed: {gameover}", color=(1, 1, 0))  

def convert_coordinate(x, y): # alternative coordinate system (where the origin (0,0) is at the center of the screen)
    global W_WIDTH, W_HEIGHT
    a = x - (W_WIDTH / 2)
    b = (W_HEIGHT / 2) - y
    return a, b


def keyboardListener(key, x, y):
    global firing_ball, pause, gameover, catcher
    if key == b' ':
        if not pause and gameover < 3:
            firing_ball.append([catcher.x, -365 + 60]) #adds a new firing_ball to the firing_ball list
    elif key == b'a':
        if catcher.x > -230 and not pause:
            catcher.x -= 10 # moving the catcher left by decreasing its x-coordinate by 10 pixel
    elif key == b'd':
        if catcher.x < 230 and not pause:
            catcher.x += 10
    glutPostRedisplay()

def mouseListener(button, state, x, y): #restart, pause and game cancel er kaaj ekhane hoi
    global pause, gameover, catcher, score, bubble, firing_ball, missed_fire_shot 
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            pause = False
            print('Starting Over the game')
            bubble = [Falling_balls(), Falling_balls(), Falling_balls(), Falling_balls(), Falling_balls()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            missed_fire_shot  = 0
            firing_ball = []
        if 170 < c_x < 216 and 330 < c_y < 370:
            #show_goodbye_message = True
            print('Goodbye! Final Score:', score)           
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            pause = not pause
    glutPostRedisplay()


def render_text(x, y, text, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_firing_ball()
    draw_bubble()
    if gameover >= 3 or missed_fire_shot  >= 3: #gameover er condition
        render_text(-40, 50, "Game Over!", color=(1, 0, 0))  
    glutSwapBuffers()


def animate(): #game state update korar jonno
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0 # smooth animation er jonno
    animate.start_time = current_time #Stores the time of the last animation update.

    global pause, bubble, catcher, gameover, score, firing_ball, missed_fire_shot , bonus_ball, bonus_ball_timer, expand
    if not pause and gameover < 3 and missed_fire_shot  < 3:
        delidx = []
        for i in range(len(firing_ball)):
            if firing_ball[i][1] < 400:
                firing_ball[i][1] += 10  #firing_ball Movement
            else:
                delidx.append(i)
                missed_fire_shot  += 1
        try:
            for j in delidx:
                del firing_ball[j] #bullet delete
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400: # bubble within the game boundary
                    bubble[i].y -= (10 + score * 5) * delta_time # 
                else:
                    gameover += 1 #boundary cross kora
                    del bubble[i] # 
                    bubble.append(Falling_balls()) # 
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (  # 
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Falling_balls())
                    bubble.sort(key=lambda b: b.y)


        if not bonus_ball and random.random() < 0.01: #a special bubble
            bonus_ball =Bonus_ball() # create a new Bonus_ball.
        
        if bonus_ball:
            if bonus_ball.y > -400:
                bonus_ball.y -= (10 + score * 5) * delta_time # Moves the bonus_ball down the screen and also speed increase

                if expand:
                    bonus_ball.r += 0.2 
                    if bonus_ball.r >= 30: 
                        expand = False
                else:
                    bonus_ball.r -= 0.2 # shrink shart
                    if bonus_ball.r <= 15:
                        expand = True
            else:
                bonus_ball = None # bonus_ball has moved out of boundary
                gameover += 1  
        try:
            for i in range(len(bubble)):
                spaceship_points = [ 
                    (catcher.x, -365 + 60),
                    (catcher.x - 10, -365 + 40),
                    (catcher.x + 10, -365 + 40), 
                    (catcher.x - 10, -365 - 10), 
                    (catcher.x + 10, -365 - 10), 
                    (catcher.x - 20, -365 - 30), 
                    (catcher.x + 20, -365 - 30), ]
                           
                for point in spaceship_points:  # A collision detect korar jonno spaceship er sathe
                    if abs(bubble[i].x - point[0]) < bubble[i].r and abs(bubble[i].y - point[1]) < bubble[i].r: #
                        gameover += 3 
                        break
                for j in range(len(firing_ball)): #  Detects if a firing_ball hits a bubble.
                    if abs(bubble[i].y - firing_ball[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - firing_ball[j][0]) < (bubble[i].r + 20): 
                        score += 1
                        print("Score:", score)
                        del bubble[i]
                        del firing_ball[j]
                        bubble.append(Falling_balls())
            if bonus_ball:
                for point in spaceship_points: 
                    if abs(bonus_ball.x - point[0]) < bonus_ball.r and abs(bonus_ball.y - point[1]) < bonus_ball.r:
                        gameover += 3  
                        break

                for j in range(len(firing_ball)): 
                    if abs(bonus_ball.y - firing_ball[j][1]) < (bonus_ball.r + 15) and abs(bonus_ball.x -firing_ball[j][0]) < (
                            bonus_ball.r + 20):
                        score += 3
                        print("Special Hit! Score:", score)
                        bonus_ball= None
                        del firing_ball[j]
                        break
        except:
            pass
    if (gameover >= 3 or missed_fire_shot  >= 3) and not pause: 
        print("Game Over! Score:", score)
        pause = True
        bubble = [] 
        bonus_ball= []
    time.sleep(1 / 1000) 
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)

glutInit()
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Shoot The Circles Game!")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()