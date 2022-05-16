from collections import deque

import pygame.gfxdraw
import math

class Planet(object):

    x_vel = 0
    y_vel = 0

    AU = 149597870700 # Astronomical unit
    SCALE = 250/AU
    G = 6.67428e-11  # Gravitational constant

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius*2
        self.color = color
        self.mass = mass
        self.orbit = deque([])

        self.sun_distance = 0
        self.is_sun = False
        self.image = False

    def converted_pos(self, win):
        x = int(self.x * self.SCALE) + win.get_width() // 2
        y = int(self.y * self.SCALE) + win.get_height() // 2
        return x, y

    def distance(self, planet2):
        x1, y1 = self.x, self.y
        x2, y2 = planet2.x, planet2.y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def gravitational_force(self, planet2):
        distance = self.distance(planet2)
        if planet2.is_sun:
            self.sun_distance = distance

        total_force = (self.G * self.mass * planet2.mass) / (distance ** 2)

        x_distance = planet2.x - self.x
        y_distance = planet2.y - self.y

        sin = y_distance / distance
        cos = x_distance / distance

        x_force = total_force * cos
        y_force = total_force * sin

        return x_force, y_force

    def draw(self, win):
        x, y = self.converted_pos(win)
        if self.image:
            win.blit(self.image, (x - self.radius, y - self.radius))
        else:
            radius = int(self.radius) + 1
            pygame.gfxdraw.filled_circle(win, x, y, radius, self.color)

    def add_orbit(self, pos):
        if len(self.orbit) > 700:
            self.orbit.popleft()
        self.orbit.append(pos)