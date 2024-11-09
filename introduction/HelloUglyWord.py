import pygame, sys
from pygame.locals import *

pygame.init()
displaysurf = pygame.display.set_mode((400, 300))
pygame.display.set_caption('HelloUglyWord')

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj= fontObj.render('hello ugly word', True, green, blue)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

#game loop
while True:
    displaysurf.fill(white)
    displaysurf.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()