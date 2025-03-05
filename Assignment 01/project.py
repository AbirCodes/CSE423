import sys
import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Game state variables
screen_width = 800
screen_height = 600
balls = []  # Cluster of balls at the top
bullets = []  # Balls being fired
shooter_angle = 0
game_over = False
ball_colors = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0)]  # Red, Blue, Yellow, Purple

# Ball class for cluster and bullets
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Function to draw a ball
def draw_ball(ball):
    glColor3f(*ball.color)
    glBegin(GL_POLYGON)
    num_segments = 50
    radius = 20  # Radius of the ball
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        glVertex2f(ball.x + math.cos(angle) * radius, ball.y + math.sin(angle) * radius)
    glEnd()

# Function to draw the shooter
def draw_shooter():
    glPushMatrix()
    glTranslatef(0, -screen_height // 2 + 50, 0)
    glRotatef(shooter_angle, 0, 0, 1)
    
    # Rocket body
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-20, 0)
    glVertex2f(20, 0)
    glVertex2f(20, 100)
    glVertex2f(-20, 100)
    glEnd()

    # Rocket tip
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-20, 100)
    glVertex2f(20, 100)
    glVertex2f(0, 130)
    glEnd()

    glPopMatrix()

# Function to draw a line using the Midpoint Line Algorithm
def draw_line(x1, y1, x2, y2):
    # Midpoint Line Algorithm for drawing lines between two points
    dx = x2 - x1
    dy = y2 - y1
    p = 2 * dy - dx
    x = x1
    y = y1
    glVertex2f(x, y)

    while x < x2:
        x += 1
        if p < 0:
            p += 2 * dy
        else:
            y += 1
            p += 2 * (dy - dx)
        glVertex2f(x, y)

# Function to initialize the cluster of balls within boundaries
def init_cluster():
    balls = []
    # Calculate boundaries for the cluster to fit inside the window
    x_start = -screen_width // 4
    x_end = screen_width // 4
    y_start = screen_height // 3
    y_end = screen_height // 2

    # Generate balls in a grid between these boundaries
    for x in range(x_start, x_end, 40):  # Horizontal spacing (adjust for desired cluster size)
        for y in range(y_start, y_end, 40):  # Vertical spacing
            balls.append(Ball(x, y, random.choice(ball_colors)))

    return balls

# Display function
def display():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(-50, 0)
        for c in "Game Over":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        glutSwapBuffers()
        return

    # Draw all balls in the cluster
    for ball in balls:
        draw_ball(ball)

    # Draw all bullets
    for bullet in bullets:
        draw_ball(bullet)

    # Draw the shooter
    draw_shooter()

    glutSwapBuffers()

# Update function for animation
def update(value):
    global bullets, balls, game_over

    if game_over:
        return

    # Move bullets
    for bullet in bullets[:]:
        bullet.x += math.sin(math.radians(-shooter_angle)) * 5
        bullet.y += math.cos(math.radians(-shooter_angle)) * 5

        # Check for collision with cluster
        for ball in balls[:]:
            distance = math.sqrt((bullet.x - ball.x)**2 + (bullet.y - ball.y)**2)
            if distance <= 40:  # Collision detected
                bullets.remove(bullet)
                balls.remove(ball)  # Destroy the ball in the cluster
                break

        # Remove bullets if they move out of bounds
        if bullet.y > screen_height // 2 or bullet.x < -screen_width // 2 or bullet.x > screen_width // 2:
            bullets.remove(bullet)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# Mouse input for shooter rotation
def mouse(button, state, x, y):
    global shooter_angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if shooter_angle < 90:  # Ensure the shooter doesn't bend further right than +90 degrees
            shooter_angle += 10
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if shooter_angle > -90:  # Ensure the shooter doesn't bend further left than -90 degrees
            shooter_angle -= 10
    glutPostRedisplay()

# Fire bullets with the space bar
# Fire bullets with the space bar
# Fire bullets with the space bar
def keyboard(key, x, y):
    global shooter_angle, bullets

    # Shooter base coordinates for the top of the triangle part of the rocket
    shooter_base_x = 0
    shooter_base_y = -screen_height // 2 + 50  # The base of the rocket's body

    # New origin point for the bullet (move slightly to the left or right)
    offset_x = 30  # Change this to control horizontal offset
    offset_y = 30  # Change this to control vertical offset

    # Calculate new origin point for the bullet (tip of the triangle)
    triangle_tip_x = shooter_base_x + math.sin(math.radians(shooter_angle)) * (-130 + offset_x)  # Adjust origin with offset
    triangle_tip_y = shooter_base_y + math.cos(math.radians(shooter_angle)) * (130 + offset_y)  # Adjust origin with offset

    if key == b' ':
        # Create a new green bullet from the adjusted origin point
        new_bullet = Ball(triangle_tip_x, triangle_tip_y, (0.0, 1.0, 0.0))  # Green color for bullets
        bullets.append(new_bullet)

    glutPostRedisplay()


# Initialize OpenGL and set up the game
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-screen_width // 2, screen_width // 2, -screen_height // 2, screen_height // 2)

# Main function
def main():
    global balls
    balls = init_cluster()  # Create the cluster of balls within boundaries

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screen_width, screen_height)
    glutCreateWindow(b"Bubble Shooter with Cluster within Bounds")

    init()

    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)

    glutMainLoop()


if __name__ == "_main_":
    main()

