# Extended rectangle class

import pygame

class Rect:
    """A rectangle centred at (cx, cy) with width w and height h."""

    def __init__(self, cx, cy, w, h):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.west_edge, self.east_edge = cx - w / 2, cx + w / 2
        self.north_edge, self.south_edge = cy - h / 2, cy + h / 2

        self.color = (255, 255, 0)
        self.contours = pygame.Rect(self.west_edge, self.north_edge, self.w, self.h)
        self.dist = 2

    def __repr__(self):
        return str((self.west_edge, self.east_edge, self.north_edge, self.south_edge))

    def __str__(self):
        return "({:.2f}, {:.2f}, {:.2f}, {:.2f})".format(
            self.west_edge, self.north_edge, self.east_edge, self.south_edge
        )

    def contains(self, point):
        """Is point (a Point object or (x,y) tuple) inside this Rect?"""

        try:
            point_x, point_y = point.x, point.y
        except AttributeError:
            point_x, point_y = point

        return (
            point_x >= self.west_edge
            and point_x < self.east_edge
            and point_y >= self.north_edge
            and point_y < self.south_edge
        )

    def intersects(self, other):
        return not (
            other.west_edge > self.east_edge
            or other.east_edge < self.west_edge
            or other.north_edge > self.south_edge
            or other.south_edge < self.north_edge
        )

    def handle_input(self):

        key = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if key[pygame.K_EQUALS]:
           self.dist = 3
           print("MOVE SPEED INCREASED", self.dist)

        if key[pygame.K_MINUS]:
           self.dist = 1
           print("MOVE SPEED DECREASED", self.dist)
        
        if key[pygame.K_a]:
           self.contours.move_ip(-self.dist, 0)
           dx = -self.dist
        if key[pygame.K_d]:
           self.contours.move_ip(self.dist, 0)
           dx = self.dist
        if key[pygame.K_w]:
           self.contours.move_ip(0, -self.dist)
           dy = -self.dist
        if key[pygame.K_s]:
           self.contours.move_ip(0, self.dist)
           dy = self.dist
        return [dx, dy]


    def draw(self, p1, p2, window):
        x = p1[0]
        y = p1[1]
        w = p2[0] - x
        h = p2[1] - y

        pygame.draw.rect(window, self.color, pygame.Rect(x, y, w, h), 2)

    def collidePoint(self, x, y, radius, window):

        color = [0, 255, 0]

        # Colors points within box green
        if self.contours.collidepoint(x,y):
            pygame.draw.circle(window, self.color, (x, y), radius)
        else:
            pygame.draw.circle(window, color, (x, y), radius)