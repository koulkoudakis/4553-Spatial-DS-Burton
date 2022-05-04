import pygame
import random
from pygame import *

from pyRect import Rect

pygame.init()

pygame.display.set_caption('PO7')

screen_width, screen_height = 690, 420
window = pygame.display.set_mode((screen_width, screen_height))

#create random points

points = []

toPoints = int((screen_width // 100) * (screen_height//100)*2.5)

# creating points for processing
for point in range(toPoints):    
    circleX = random.randint(0, 690)
    circleY = random.randint(0, 420)
    radius = random.randint(5, 20)

    points.append([circleX, circleY])

results = []

font = pygame.font.Font('freesansbold.ttf', 20)

# create a text surface object,
# on which text is drawn on it.
text = font.render('Click LMB : draw rectangle, Movement : WASD, Change Speed : +/-', True, (0,0,0), (255,255,255))
textRect = text.get_rect()

v = [2, 0]


selection = Rect((screen_width//2), (screen_height//2), 0, 0)

two_points = False
num_clicks = 0


p1_selection = [screen_width//2, screen_height//2]
p2_selection = [screen_width, screen_height]

def mouse_bbox(event, num_clicks, p1_selection, p2_selection, two_points):

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
            print("LMB\n")
            num_clicks += 1

            if num_clicks != 0:
                if num_clicks % 2 == 0:
                    two_points = True

                    selection = Rect((((p1_selection[0] + p2_selection[0]) // 2)), ((p1_selection[1] + p2_selection[1]) // 2),
                                abs(p2_selection[0] - p1_selection[0]), abs(p2_selection[1] - p1_selection[1]))
                    print(f'selection: ', selection)

                else:
                    two_points = False
                    p1_selection = list(pygame.mouse.get_pos())

            print(p1_selection, p2_selection)

    return num_clicks, p1_selection, p2_selection, two_points

done = False

while not done:

    for event in pygame.event.get():

        # num_clicks, p1_selection, p2_selection, two_points = mouse_bbox(event, num_clicks, p1_selection, p2_selection, two_points)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                print("LMB clicked \n")
                num_clicks += 1

                if num_clicks != 0:
                    if num_clicks % 2 == 0:
                        two_points = True

                        p2_selection = list(pygame.mouse.get_pos())

                        selection = Rect(( ((p1_selection[0] + p2_selection[0]) // 2)), ((p1_selection[1] + p2_selection[1]) // 2), abs(p2_selection[0] - p1_selection[0]), abs(p2_selection[1] - p1_selection[1]))
                        print(f'selection: ', selection)

                    else:
                        two_points = False
                        p1_selection = list(pygame.mouse.get_pos())

                print(p1_selection, p2_selection)

    window.fill((255,255,255))

    if two_points:
        delta = selection.handle_input()

        p1_selection[0] += delta[0]
        p2_selection[0] += delta[0]
        p1_selection[1] += delta[1]
        p2_selection[1] += delta[1]

        selection.draw(p1_selection, p2_selection, window)

    for x, y in points:

        selection.collidePoint(x, y, radius, window)

    window.blit(text, textRect)
          
    pygame.display.update() 

    pygame.display.flip()
pygame.quit()






