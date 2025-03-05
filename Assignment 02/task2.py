import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import random
import time

# Screen dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game constants
CIRCLE_RADIUS = 20.0
UNIQUE_RADIUS_CHANGE = 5.0
SHOOTER_WIDTH = 40
SHOOTER_HEIGHT = 20
SHOOTER_SPEED = 10
PROJECTILE_SPEED = 8.0
FALLING_SPEED = 2.0

# Game variables
shooter_x = WINDOW_WIDTH / 2
projectiles = []
falling_circles = []
score = 0
missed_circles = 0
misfires = 0
game_over = False

# Falling circle class
class Circle:
    def __init__(self, x, y, radius, is_unique):
        self.x = x
        self.y = y
        self.radius = radius
        self.is_unique = is_unique

# Function to draw a circle
def draw_circle(x, y, radius):
    glBegin(GL_POLYGON)
    for angle in range(360):
        angle_rad = math.radians(angle)
        glVertex2f(x + math.cos(angle_rad) * radius, y + math.sin(angle_rad) * radius)
    glEnd()

# Function to draw the shooter
def draw_shooter(x):
    glColor3f(0.0, 1.0, 0.0)  # Green shooter
    glBegin(GL_QUADS)
    glVertex2f(x - SHOOTER_WIDTH / 2, 10)
    glVertex2f(x + SHOOTER_WIDTH / 2, 10)
    glVertex2f(x + SHOOTER_WIDTH / 2, 10 + SHOOTER_HEIGHT)
    glVertex2f(x - SHOOTER_WIDTH / 2, 10 + SHOOTER_HEIGHT)
    glEnd()

# Spawn a new falling circle
def spawn_circle():
    x = random.randint(50, WINDOW_WIDTH - 50)
    y = WINDOW_HEIGHT
    is_unique = random.random() < 0.2  # 20% chance to be unique
    falling_circles.append(Circle(x, y, CIRCLE_RADIUS, is_unique))

# Update falling circles
def update_circles():
    global missed_circles, game_over
    for circle in falling_circles:
        circle.y -= FALLING_SPEED
        if circle.is_unique:
            # Pulsating effect for unique circles
            circle.radius = CIRCLE_RADIUS + UNIQUE_RADIUS_CHANGE * math.sin(time.time() * 5)
        if circle.y + circle.radius < 0:
            falling_circles.remove(circle)
            missed_circles += 1
            if missed_circles >= 3:
                game_over = True

# Update projectiles
def update_projectiles():
    for projectile in projectiles:
        projectile.y += PROJECTILE_SPEED
        if projectile.y > WINDOW_HEIGHT:
            projectiles.remove(projectile)

# Check collisions between projectiles and circles
def check_collisions():
    global score, game_over
    for circle in falling_circles[:]:
        for projectile in projectiles[:]:
            dx = circle.x - projectile.x
            dy = circle.y - projectile.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= circle.radius:
                if circle.is_unique:
                    score += 10  # Bonus points for unique circles
                else:
                    score += 1
                falling_circles.remove(circle)
                projectiles.remove(projectile)
                break

# Display the score and game over message
def display_text(text, x, y):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Render the game
def render():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the shooter
    draw_shooter(shooter_x)

    # Draw projectiles
    glColor3f(1.0, 0.0, 0.0)  # Red projectiles
    for projectile in projectiles:
        draw_circle(projectile.x, projectile.y, 5)

    # Draw falling circles
    for circle in falling_circles:
        glColor3f(1.0, 1.0, 0.0) if circle.is_unique else glColor3f(0.0, 0.0, 1.0)
        draw_circle(circle.x, circle.y, circle.radius)

    # Display score
    glColor3f(1.0, 1.0, 1.0)
    display_text(f"Score: {score}", -WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 - 20)

    # Game over message
    if game_over:
        display_text("Game Over!", -50, 0)
        display_text(f"Final Score: {score}", -60, -30)

    glutSwapBuffers()

# Handle keyboard input
def keyboard(key, x, y):
    global shooter_x, projectiles, game_over
    if game_over:
        return
    if key == b'a' and shooter_x - SHOOTER_WIDTH / 2 > 0:
        shooter_x -= SHOOTER_SPEED
    elif key == b'd' and shooter_x + SHOOTER_WIDTH / 2 < WINDOW_WIDTH:
        shooter_x += SHOOTER_SPEED
    elif key == b' ':
        # Shoot a projectile
        projectiles.append(Circle(shooter_x, 10 + SHOOTER_HEIGHT, 5, False))

# Main game loop
def game_loop():
    global game_over
    if not game_over:
        update_circles()
        update_projectiles()
        check_collisions()
    render()
    glutPostRedisplay()
    glutTimerFunc(16, lambda x: game_loop(), 0)

# Initialize the game
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

# Main function
def main():
    global falling_circles
    pygame.init()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Shoot The Circles!")
    glutDisplayFunc(render)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, lambda x: game_loop(), 0)
    init()

    # Spawn circles periodically
    def spawn_task():
        if not game_over:
            spawn_circle()
            pygame.time.set_timer(USEREVENT + 1, 1000)

    spawn_task()
    glutMainLoop()

if __name__ == "__main__":
    main()
