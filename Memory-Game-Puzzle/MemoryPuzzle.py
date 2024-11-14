import random
import pygame
import sys
from pygame.locals import *

# Initialize colors, shapes, and settings
FPS = 30 #frames per second
windowwidth = 640 #window width size in pixels
windowheight = 480
revealspeed = 8 #speed of boxes sliding reveals and covers
boxsize = 40 #height and width of boxes in pixels
gapsize = 10
boardwidth = 10 #number of columns of icons
boardheight = 7 #number of rows of icons

assert (boardwidth * boardheight) % 2 == 0, 'Board needs an even number of boxes for matching pairs'
xmargin = int((windowwidth - (boardwidth * (boxsize + gapsize))) / 2)
ymargin = int((windowheight - (boardheight * (boxsize + gapsize))) / 2)

# Colors RGB
gray = (100, 100, 100)
navyblue = (60, 60, 100)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)

backgroundcolor = navyblue
lightbackgroundcolor = gray
boxcolor = white
highlightcolor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allcolors = (red, green, blue, yellow, orange, purple, cyan)
allshapes = (donut, square, diamond, lines, oval)

assert len(allcolors) * len(allshapes) * 2 >= boardwidth * boardheight, 'Board is too big for the number of shapes/colors defined'

# Game functions
def main():
    global FPSClock, displaysurf
    pygame.init()
    FPSClock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowwidth, windowheight))

    pygame.display.set_caption('Memory Game')
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxes(False)

    firstSelection = None
    displaysurf.fill(backgroundcolor)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False
        displaysurf.fill(backgroundcolor)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True

                if firstSelection is None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, *firstSelection)
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [firstSelection, (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxes(False)
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                    firstSelection = None
        pygame.display.update()
        FPSClock.tick(FPS)

def generateRevealedBoxes(isRevealed):
    # Returns a 2D list with 'isRevealed' value for each box
    return [[isRevealed] * boardheight for _ in range(boardwidth)]

def getRandomizedBoard():
    # Get a list of every possible shape in every possible color
    icons = [(color, shape) for color in allcolors for shape in allshapes]
    random.shuffle(icons)
    numIconsUsed = boardwidth * boardheight // 2
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons
    return [[icons.pop() for _ in range(boardheight)] for _ in range(boardwidth)]

def leftTopCoordsOfBox(boxx, boxy):
    # Convert box coordinates into pixel coordinates
    left = boxx * (boxsize + gapsize) + xmargin
    top = boxy * (boxsize + gapsize) + ymargin
    return left, top

def getBoxAtPixel(x, y):
    # Check if the mouse click is inside a box
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxrect = pygame.Rect(left, top, boxsize, boxsize)
            if boxrect.collidepoint(x, y):
                return boxx, boxy
    return None, None

def drawIcon(shape, color, boxx, boxy):
    # Draw the shapes
    quarter = boxsize // 4
    half = boxsize // 2
    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == donut:
        pygame.draw.circle(displaysurf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(displaysurf, backgroundcolor, (left + half, top + half), quarter - 5)
    elif shape == square:
        pygame.draw.rect(displaysurf, color, (left + quarter, top + quarter, boxsize - half, boxsize - half))
    elif shape == diamond:
        pygame.draw.polygon(displaysurf, color, ((left + half, top), (left + boxsize - 1, top + half), (left + half, top + boxsize - 1), (left, top + half)))
    elif shape == lines:
        for i in range(0, boxsize, 4):
            pygame.draw.line(displaysurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(displaysurf, color, (left + i, top + boxsize - 1), (left + boxsize - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(displaysurf, color, (left, top + quarter, boxsize, half))

def getShapeAndColor(board, boxx, boxy):
    # Shape and color values for x, y spot are stored in board[x][y][0] and board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(displaysurf, backgroundcolor, (left, top, boxsize, boxsize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        # Adding color validation
        if isinstance(color, tuple) and len(color) == 3:
            pygame.draw.rect(displaysurf, color, (left, top, coverage, boxsize))
        else:
            print(f"Invalid color: {color}")  # Debugging output
    pygame.display.update()
    FPSClock.tick(FPS)

def revealBoxesAnimation(board, boxestoreveal):
    # Box reveal animation
    for coverage in range(boxsize, (-revealspeed) - 1, -revealspeed):
        drawBoxCovers(board, boxestoreveal, coverage)

def coverBoxesAnimation(board, boxestocover):
    # Box cover animation
    for coverage in range(0, boxsize + revealspeed, revealspeed):
        drawBoxCovers(board, boxestocover, coverage)

def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(displaysurf, backgroundcolor, (left, top, boxsize, boxsize)) # Draw covered box
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(displaysurf, highlightcolor, (left - 5, top - 5, boxsize + 10, boxsize + 10), 4)

def startGameAnimation(board):
    # Initial random boxes animation
    coveredBoxes = generateRevealedBoxes(False)
    boxes = [(x, y) for x in range(boardwidth) for y in range(boardheight)]
    random.shuffle(boxes)
    boxGroups = [boxes[i:i + 8] for i in range(0, len(boxes), 8)]
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    # Flashes the background color when the player wins
    coveredBoxes = generateRevealedBoxes(True)
    color1 = lightbackgroundcolor
    color2 = backgroundcolor
    for i in range(13):
        color1, color2 = color2, color1
        displaysurf.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # Returns True if all boxes are revealed, False otherwise
    return all(all(row) for row in revealedBoxes)

if __name__ == '__main__':
    main()
