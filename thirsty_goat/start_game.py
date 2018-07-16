import os
import pygame
from classes import Farm, Characters

play = True

#def get_input_continue(farm):
#    prompt_str = "Current map:\n" + \
#                 str(farm) + "\n" * 2 + \
#                "Which way would you like to go? (" + ", ".join(farm.find_possible_directions()) + "): "
#    return input(prompt_str)

current_farm = Farm.FarmMap()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 100
HEIGHT = 100
 
# This sets the margin between each cell
MARGIN = 5
 
nrows = current_farm._layout.shape[0]
ncols = current_farm._layout.shape[1]
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
X_SIZE = WIDTH * ncols + MARGIN * (ncols + 1)
Y_SIZE = HEIGHT * nrows + MARGIN * (nrows + 1)
WINDOW_SIZE = [X_SIZE, Y_SIZE]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Thirsty Goat!")
 
# Loop until the user clicks the close button.
done = False
won = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

import os
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

goat = pygame.image.load('data/goat-100x100.png')
water = pygame.image.load('data/water-100x95.png')
    
while not done:
    while not won:
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                done = True
            elif e.type == pygame.KEYDOWN:
                next_dir = None
                if e.key == pygame.K_DOWN and 'Down' in current_farm.find_possible_directions():
                    next_dir = 'Down'
                elif e.key == pygame.K_UP and 'Up' in current_farm.find_possible_directions():
                    next_dir = 'Up'
                elif e.key == pygame.K_RIGHT and 'Right' in current_farm.find_possible_directions():
                    next_dir = 'Right'
                elif e.key == pygame.K_LEFT and 'Left' in current_farm.find_possible_directions():
                    next_dir = 'Left'
                
                if next_dir:
                    try:
                        current_farm.move(next_dir)
                    except OverflowError:
                        won = True
     
        # Set the screen background
        screen.fill(BLACK)
     
        # Draw the current_farm
        for row in range(nrows):
            for column in range(ncols):
                color = WHITE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                if isinstance(current_farm._layout[row][column]._unit, Characters.Player):
                    screen.blit(goat, [(MARGIN + WIDTH) * column + MARGIN,
                                       (MARGIN + HEIGHT) * row + MARGIN,
                                       WIDTH,
                                       HEIGHT])
        if won:
            fountain_loc = current_farm.find_fountain()
            screen.blit(water, [(MARGIN + WIDTH) * fountain_loc[0] + MARGIN,
                                (MARGIN + HEIGHT) * fountain_loc[1] + MARGIN + (HEIGHT - 95) / 2,
                                WIDTH,
                                HEIGHT])          
            if pygame.font:
                font = pygame.font.Font(None, 30)
                text = font.render("Thirst Quenched!", True, RED)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
     
        # Limit to 60 frames per second
        clock.tick(60)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    if pygame.event.wait().type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
        break

pygame.quit()