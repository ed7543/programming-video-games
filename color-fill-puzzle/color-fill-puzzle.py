import random
import pygame, sys
from pygame.locals import *

# Initialize settings, shapes, and colors
FPS = 30
windowWidth = 640
windowHeight = 480
boxSize = 40
gapSize = 10
boardWidth = 5
boardHeight = 5

xMargin = int((windowWidth - (boardWidth * (boxSize + gapSize))) / 2)
yMargin = int((windowHeight - (boardHeight * (boxSize + gapSize))) / 2)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (225, 47, 47)
orange = (255, 129, 55)
pink = (255, 147, 170)
lightOrange = (255, 206, 148)
lightPurple = (235, 197, 245)

colors = [red, orange, pink, lightOrange]

backgroundColor = lightPurple
borderColor = black

# Create a 2D list to track the color of each box
board = [[white for _ in range(boardWidth)] for _ in range(boardHeight)]

def generateBoard(screen):
    for row in range(boardHeight):
        for col in range(boardWidth):
            left = xMargin + col * (boxSize + gapSize)
            top = yMargin + row * (boxSize + gapSize)
            # Draw the box with the current color from the board and a black border
            pygame.draw.rect(screen, borderColor, (left, top, boxSize, boxSize), 3)  # Border
            pygame.draw.rect(screen, board[row][col], (left + 3, top + 3, boxSize - 6, boxSize - 6))  # Inside color


def colorRandomBoxes():
    # Start with a random initial box and color
    row = random.randint(0, boardHeight - 1)
    col = random.randint(0, boardWidth - 1)
    initial_color = random.choice(colors)
    board[row][col] = initial_color
    colored_positions = [(row, col)]

    # Generate 4 more neighboring boxes with different colors
    for _ in range(4):
        neighbors = []
        for r, c in colored_positions:
            potential_neighbors = [
                (r - 1, c),  # above
                (r + 1, c),  # below
                (r, c - 1),  # left
                (r, c + 1)  # right
            ]
            # Filter valid, uncolored neighbors
            for nr, nc in potential_neighbors:
                if 0 <= nr < boardHeight and 0 <= nc < boardWidth and board[nr][nc] == white:
                    neighbors.append((nr, nc))

        # If we have available neighbors, select one and color it
        if neighbors:
            row, col = random.choice(neighbors)

            # Ensure no neighboring box has the same color
            available_colors = [color for color in colors if is_valid_color(row, col, color)]
            if available_colors:
                selected_color = random.choice(available_colors)
                board[row][col] = selected_color
                colored_positions.append((row, col))


def is_valid_color(row, col, color):
    # Check neighbors
    neighbors = [
        (row - 1, col),  # above
        (row + 1, col),  # below
        (row, col - 1),  # left
        (row, col + 1),  # right
    ]

    for (i, j) in neighbors:
        if 0 <= i < boardHeight and 0 <= j < boardWidth:
            if board[i][j] == color:
                return False
    return True

def getBox(x, y):
    for row in range(boardHeight):
        for col in range(boardWidth):
            left = xMargin + col * (boxSize + gapSize)
            top = yMargin + row * (boxSize + gapSize)
            boxRect = pygame.Rect(left, top, boxSize, boxSize)
            if boxRect.collidepoint(x, y):
                return (row, col)
    return None, None

def checkWin():
    # Check if the board is fully filled and all adjacent rules are satisfied
    for row in range(boardHeight):
        for col in range(boardWidth):
            if board[row][col] == white or not is_valid_color(row, col, board[row][col]):
                return False
    return True

def winAnimation(screen):
    for i in range(10):
        screen.fill(random.choice(colors))
        pygame.display.update()
        pygame.time.delay(200)
    screen.fill(backgroundColor)

def loseAnimation(screen):
    for i in range(5):
        screen.fill(red)
        pygame.display.update()
        pygame.time.delay(100)
        screen.fill(backgroundColor)
        pygame.display.update()
        pygame.time.delay(100)

def displayIntroScreen(screen):
    screen.fill(pink)
    font = pygame.font.Font(None, 20)
    instructions = [
        "Welcome to Color Fill Puzzle!",
        "Instructions:",
        "1. Click on a box to fill it with color.",
        "2. Adjacent boxes cannot be the same color.",
        "3. Press keys (R, O, P, L) to select colors.",
        "Press 'R' for Red, 'O' for Orange, 'P' for Pink, and 'L' for Light Orange.",
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, black)
        screen.blit(text, (50, 50 + i * 40))

    # Draw Start Button
    button_font = pygame.font.Font(None, 40)
    button_text = button_font.render("Start Game", True, white)
    button_rect = pygame.Rect(windowWidth // 2 - 100, windowHeight - 100, 200, 60)
    pygame.draw.rect(screen, pink, button_rect)
    screen.blit(button_text, (button_rect.x + 25, button_rect.y + 10))

    pygame.display.update()
    return button_rect

def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Color Fill Puzzle')
    clock = pygame.time.Clock()

    # Display Intro Screen until the Start Button is clicked
    intro_active = True
    selected_color = red

    while intro_active:
        button_rect = displayIntroScreen(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y):
                    intro_active = False  # Exit intro screen

    # Color 5 random boxes with random colors
    colorRandomBoxes()

    # Main Game Loop
    while True:
        screen.fill(backgroundColor)
        generateBoard(screen)

        if checkWin():
            winAnimation(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                row, col = getBox(mouse_x, mouse_y)
                if row is not None and col is not None:
                    if board[row][col] == white and is_valid_color(row, col, selected_color):
                        board[row][col] = selected_color
                    else:
                        loseAnimation(screen)
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    selected_color = red
                elif event.key == K_o:
                    selected_color = orange
                elif event.key == K_p:
                    selected_color = pink
                elif event.key == K_l:
                    selected_color = lightOrange

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
