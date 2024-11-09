import pygame, sys
from pygame.locals import *

pygame.init()
#this function returns object for the window
DISPLAYSURF = pygame.display.set_mode((400, 300)) #this is the width and height for the window
pygame.display.set_caption('Hello World')

#the loop is for event handling
while True: #main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

#setting the title of the game
#caption is basically the title