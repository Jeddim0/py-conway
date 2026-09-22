import pygame
import random
from scripts.game import Game

# constants

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 160, 120
WINDOW_SCALE = 4
WINDOW_SIZE = SCREEN_WIDTH * WINDOW_SCALE, SCREEN_HEIGHT * WINDOW_SCALE

UPDATES_PER_SEC = 30

CELL_ALIVE = 1
CELL_DEAD = 0

ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

# init and game loop functions

def init():
    pygame.init()
    game = Game()
    game.screen = pygame.Surface(SCREEN_SIZE)
    game.window = pygame.display.set_mode(WINDOW_SIZE)
    game.clock = pygame.time.Clock()

def process_input(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

def update(game):
    m_pos = pygame.mouse.get_pos()
    
    # convert mouse pos in window to play area coords
    m_pos = (m_pos[0] // WINDOW_SCALE, m_pos[1] // WINDOW_SCALE)
    m_buttons = pygame.mouse.get_pressed()

    if m_buttons[0]:
        game.set_cell_at_coords(m_pos[0], m_pos[1], CELL_ALIVE)

    if m_buttons[2]:
        game.set_cell_at_coords(m_pos[0], m_pos[1], CELL_DEAD)

def render(game):
    # get game cell data and display it as pixels
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            cell_state = game.return_cell_from_coords(x, y)
            if cell_state == CELL_ALIVE:
                game.screen.set_at((x, y), ALIVE_COLOR)
            else:
                game.screen.set_at((x, y), DEAD_COLOR)

    # resize play area to window size and display    
    game.window.blit(pygame.transform.scale(game.screen, WINDOW_SIZE), (0, 0))
    pygame.display.flip()

def main():
    init()
    game = Game()
    # populate cell list based on size of the play area
    for i in range(SCREEN_HEIGHT * SCREEN_WIDTH):
        game.cells.append(CELL_DEAD)

    game.running = True

    while game.running:
        process_input(game)
        update(game)
        render(game)

    pygame.quit()

if __name__ == "__main__":
    main()
