# import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dy < 0 and dx >= dy:
        return 1
    elif dy >= 0 and dx >= dy:
        return 2
    elif dy >= dx and dx >= 0:
        return 3
    elif dy >= dx and dx < 0:
        return 4
    elif dy < 0 and dx < dy:
        return 5
    elif dy < 0 and dx >= -dy:
        return 6
    elif dy >= 0 and dx <= -dy:
        return 7
    elif dy >= -dx and dx < 0:
        return 8

def transform_to_zone0(x, y, zone):
    if zone == 1:
        return x, -y
    elif zone == 2:
        return x, y
    elif zone == 3:
        return y, x
    elif zone == 4:
        return -y, x
    elif zone == 5:
        return -x, -y
    elif zone == 6:
        return -x, y
    elif zone == 7:
        return -y, -x
    elif zone == 8:
        return y, -x

def transform_from_zone0(x0, y0, zone):
    if zone == 1:
        return x0, -y0
    elif zone == 2:
        return x0, y0
    elif zone == 3:
        return y0, x0
    elif zone == 4:
        return -y0, x0
    elif zone == 5:
        return -x0, -y0
    elif zone == 6:
        return -x0, y0
    elif zone == 7:
        return -y0, -x0
    elif zone == 8:
        return y0, -x0

def mid_point_line_drawing(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1
    y = y1

    points = [(x, y)]
    while x < x2:
        if d <= 0:
            d += incE
            x += 1
        else:
            d += incNE
            x += 1
            y += 1
        points.append((x, y))

    return points