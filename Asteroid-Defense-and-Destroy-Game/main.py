from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random

boss_bullets = []
boss_bullet_speed = 0.3
boss_shoot_timer = 0
boss_shoot_interval = 120
lives = 3
height = 600
width = 800
boss_respawn_score = 10
x_astro, y_astro = 727, 488
x_target, y_target = 0, 0
asteroid_fall = False
asteroids = []
power_up_asteroid = 0
g = 9.8
v0 = 85
angle = 45
bullets = []
aliens = [] 
alien_speed = 0.5
aliens = []
alien_speed = 0.1
alien_spawn_time = 120
alien_timer = 0
score = 0
GameOver = False
bullet_speed = 0.05
flag = True
high_score = 0
boss_enemy = None
boss_health = 5
boss_speed = 0.1
boss_spawned = False

def zone_check(x0, y0, x1, y1):
    x_t0 = x0
    x_t1 = x1
    y_t0 = y0
    y_t1 = y1
    dy = y1 - y0
    dx = 1
    if x1 != x0:
        dx = x1 - x0
    slope = dy / dx
    zone1 = zone2 = zone3 = False
    if slope > 1:
        x_t0, y_t0, x_t1, y_t1 = y0, x0, y1, x1
        zone1 = True
    elif slope < -1:
        x_t0, x_t1, y_t0, y_t1 = -y0, -y1, x0, x1
        zone2 = True
    elif -1 <= slope < 0:
        x_t0, x_t1, y_t0, y_t1 = x0, x1, -y0, -y1
        zone3 = True
    return [x_t0, y_t0, x_t1, y_t1, zone1, zone2, zone3]

def mpl(x0, y0, x1, y1):
    x_t0, y_t0, x_t1, y_t1, zone1, zone2, zone3 = zone_check(x0, y0, x1, y1)
    dy = y_t1 - y_t0
    dx = 1 if x_t0 == x_t1 else x_t1 - x_t0
    d = (2 * dy) - dx
    x, y = x_t0, y_t0
    while x <= x_t1:
        if zone1:
            glVertex2f(y, x)
        elif zone2:
            glVertex2f(y, -x)
        elif zone3:
            glVertex2f(x, -y)
        else:
            glVertex2f(x, y)
        if d >= 0:
            d += (2 * dy) - (2 * dx)
            x += 1
            y += 1
        else:
            d += 2 * dy
            x += 1

def octant_points(cx, cy, x, y):
    glVertex2f(cx + x, cy + y)
    glVertex2f(cx - x, cy + y)
    glVertex2f(cx + x, cy - y)
    glVertex2f(cx - x, cy - y)
    glVertex2f(cx + y, cy + x)
    glVertex2f(cx - y, cy + x)
    glVertex2f(cx + y, cy - x)
    glVertex2f(cx - y, cy - x)

def mpc(cx, cy, r):
    d = 1 - r
    x, y = 0, r
    while x <= y:
        octant_points(cx, cy, x, y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

def draw_projectile(x, y):
    r = 5
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(2)
    glBegin(GL_POINTS)
    mpc(x, y, r)
    glEnd()

def showbullet():
    for bullet in bullets:
        t = bullet['t']
        px = bullet['x'] - bullet['vx'] * t
        py = bullet['y'] + bullet['vy'] * t - 0.5 * g * t ** 2
        draw_projectile(px, py)

def render_text(x, y, text, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def updated_points(x0, y0, length, angle):
    angle_rad = math.radians(angle)
    x1 = x0 + length * math.cos(-angle_rad)
    y1 = y0 + length * math.sin(-angle_rad)
    return x1, y1

def draw_cannon():
    global angle
    x1, y1 = 700, 50
    mpc(x1, y1, 30)
    barrel_length = 100
    x0, y0 = updated_points(x1, y1, -barrel_length, angle)
    mpl(int(x0), int(y0) + 10, int(x1), int(y1) + 30)
    mpl(int(x0), int(y0) - 10, int(x1), int(y1) - 30)
    mpc(x0, y0, 10)

def draw_alien(x, y):
    r = 10
    mpc(x, y, r)
    mpl(x - r, y, x, 40)
    mpl(x, 40, x + r, y)

def spawn_alien():
    x = random.randint(30, 200)
    aliens.append({'x': x, 'y': 80})

def spawn_boss():
    global boss_enemy, boss_health, boss_spawned, boss_respawn_score
    if score >= boss_respawn_score and not boss_spawned:
        boss_enemy = {'x': 50, 'y': 300}
        boss_health = 3
        boss_spawned = True

def draw_boss(x, y):
    glColor3f(1, 0, 0)
    glPointSize(3)
    glBegin(GL_POINTS)
    mpc(x, y, 40)
    glEnd()
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    mpc(x - 10, y + 10, 5)
    mpc(x + 10, y + 10, 5)
    glEnd()
    glColor3f(0, 0, 0)
    glBegin(GL_POINTS)
    mpc(x - 10, y + 10, 2)
    mpc(x + 10, y + 10, 2)
    glEnd()

def boss_shoot():
    global boss_enemy, boss_bullets
    if boss_enemy:
        cannon_x, cannon_y = 700, 50
        dx = cannon_x - boss_enemy['x']
        dy = cannon_y - boss_enemy['y']
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx /= dist
            dy /= dist
        boss_bullets.append({'x': boss_enemy['x'], 'y': boss_enemy['y'], 'dx': dx, 'dy': dy})
def move_boss_bullets():
    global boss_bullets, lives, GameOver
    cannon_x, cannon_y = 700, 50
    new_bullets = []
    for bullet in boss_bullets:
        bullet['x'] += bullet['dx'] * boss_bullet_speed
        bullet['y'] += bullet['dy'] * boss_bullet_speed
        dist = math.sqrt((bullet['x'] - cannon_x)**2 + (bullet['y'] - cannon_y)**2)
        if dist <= 30:
            lives -= 1
            if lives <= 0:
                GameOver = True
        elif 0 <= bullet['x'] <= width and 0 <= bullet['y'] <= height:
            new_bullets.append(bullet)
    boss_bullets = new_bullets

def draw_boss_bullets():
    glColor3f(1, 0, 1)
    glPointSize(5)
    glBegin(GL_POINTS)
    for bullet in boss_bullets:
        glVertex2f(bullet['x'], bullet['y'])
    glEnd()

def collision_check():
    global bullets, aliens, boss_enemy, boss_health, boss_spawned, score, boss_respawn_score, boss_bullets
    i = 0
    while i < len(bullets):
        bullet = bullets[i]
        bullet_removed = False
        j = 0
        while j < len(aliens):
            alien = aliens[j]
            distance = ((bullet['current_x'] - alien['x'])**2 + (bullet['current_y'] - alien['y'])**2)**0.5
            if distance <= 20:
                score += 1
                bullets.pop(i)
                aliens.pop(j)
                bullet_removed = True
                break
            j += 1
        if boss_enemy and not bullet_removed:
            distance = ((bullet['current_x'] - boss_enemy['x'])**2 + (bullet['current_y'] - boss_enemy['y'])**2)**0.5
            if distance <= 40:
                boss_health -= 1
                bullets.pop(i)
                if boss_health <= 0:
                    score += 10
                    boss_enemy = None
                    boss_spawned = False
                    boss_respawn_score = score + 10
                    boss_health = 3
                    boss_bullets.clear()
        if not bullet_removed:
            i += 1

def collision_check_with_canon():
    global aliens, angle, score, GameOver, lives
    for i in aliens:
        x1, y1 = updated_points(700, 50, -100, angle)
        distance1 = ((i['x']-x1)**2 + (i['y'] - y1)**2)**0.5
        distance2 = ((i['x']-700)**2 + (i['y'] - 50)**2)**0.5
        if (distance1 <=10) or (distance2 <=50):
            GameOver=True
         
            power_up_asteroid=0
            aliens=[]
def animate():
    global bullets, alien_timer,asteroid_fall,x_target,y_target
    new_bullets = []
    if GameOver==False:
        for bullet in bullets:
            t = bullet['t']
            px = bullet['x'] - bullet['vx'] * t
            py = bullet['y'] + bullet['vy'] * t - 0.5 * g * t ** 2
            bullet['current_x'] = px
            bullet['current_y'] = py
            if px >= -1 and py >= -1:
                bullet['t'] += 0.02  
                new_bullets.append(bullet)

        bullets = new_bullets

        for alien in aliens:
            alien['x'] += alien_speed 

        alien_timer += 1
        if alien_timer >= alien_spawn_time:
            spawn_alien()
            alien_timer = 0

    

        collision_check()
    fall_asterroid()
       

    
    
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global angle, bullets, GameOver
    if not GameOver:
        if key == b' ':
            vx = v0 * math.cos(math.radians(angle))
            vy = v0 * math.sin(math.radians(angle))
            x1, y1 = updated_points(700, 50, -100, angle)
            bullets.append({'x': x1, 'y': y1, "vx": vx, "vy": vy, "t": 0, "current_x": x1, "current_y": y1})
        elif key == b'w':
            angle = min(angle + 5, 90)
        elif key == b's':
            angle = max(angle - 5, 0)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global asteroid_fall, x_target, y_target, asteroids, power_up_asteroid
    y = abs(y - height)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if power_up_asteroid > 0:
            asteroid_fall = True
            x_target, y_target = x, y
            asteroids.append([x_target, y_target])
            power_up_asteroid -= 1
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    global bullets, GameOver, asteroid_fall, power_up_asteroid, score, boss_enemy
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    iterate()
    glColor(0, 1, 0)
    if GameOver:
        glColor(1, 0, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    draw_cannon()
    glEnd()
    render_text(10, 510, f"Score: {score}", color=(1, 1, 1))
    render_text(650, 510, f"Lives: {lives}", color=(1, 0, 0))
    render_text(300, 510, f"High Score: {high_score}", color=(1, 1, 0))
    if GameOver:
        render_text(300, 300, f"Game Over!", color=(1, 0, 0))
        render_text(300, 350, f"Final Score: {score}", color=(1, 1, 1))
    if boss_enemy:
        draw_boss(boss_enemy['x'], boss_enemy['y'])
        draw_boss_bullets()
    if not GameOver:
        showbullet()
        glPointSize(1)
        glBegin(GL_POINTS)
        glColor(1, 0, 0)
        for alien in aliens:
            draw_alien(alien['x'], alien['y'])
        glEnd()
    glutSwapBuffers()

def animate():
    global bullets, alien_timer, boss_enemy, boss_spawned, boss_speed, alien_speed, score, boss_shoot_timer
    if GameOver:
        global high_score
        if score > high_score:
            high_score = score
        return
    new_bullets = []
    for bullet in bullets:
        t = bullet['t']
        px = bullet['x'] - bullet['vx'] * t
        py = bullet['y'] + bullet['vy'] * t - 0.5 * g * t ** 2
        bullet['current_x'] = px
        bullet['current_y'] = py
        if px >= -1 and py >= -1:
            bullet['t'] += bullet_speed
            new_bullets.append(bullet)
    bullets = new_bullets
    for alien in aliens:
        alien['x'] += alien_speed
    if score >= 100:
        alien_speed = 0.2
    if boss_enemy:
        boss_enemy['x'] += boss_speed
        if boss_enemy['x'] > width:
            boss_enemy = None
            boss_spawned = False
        boss_shoot_timer += 1
        if boss_shoot_timer >= boss_shoot_interval:
            boss_shoot()
            boss_shoot_timer = 0
        move_boss_bullets()
    if not boss_enemy:
        boss_bullets.clear()
    if not boss_spawned and score >= boss_respawn_score:
        spawn_boss()
    alien_timer += 1
    if alien_timer >= alien_spawn_time:
        spawn_alien()
        alien_timer = 0
    collision_check()
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Cannon Ball Game")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()
