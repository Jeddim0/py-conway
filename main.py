# MIT License
# Copyright (c) 2026 Jeddim0


import pygame
import random
from scripts.game import Game

# constants

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 160, 120
WINDOW_SCALE = 8
WINDOW_SIZE = SCREEN_WIDTH * WINDOW_SCALE, SCREEN_HEIGHT * WINDOW_SCALE

UPDATES_PER_SEC = 30

CELL_ALIVE = 1
CELL_DEAD = 0

ALIVE_COLOR = pygame.Color('white')
DEAD_COLOR = pygame.Color('black')

# init and game loop functions

def init():
    pygame.init()
    game = Game()
    game.grid_screen = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    game.cells_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    game.window = pygame.display.set_mode(WINDOW_SIZE)
    game.clock = pygame.time.Clock()
    game.simulating = False
    game.show_grid = True

def process_input(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        if event.type == pygame.KEYDOWN:
            if not game.simulating:
                if event.key == pygame.K_k:
                    game.step_generation()
                if event.key == pygame.K_s:
                    game.save_layout()
                if event.key == pygame.K_l:
                    game.load_layout()
            if event.key == pygame.K_SPACE:
                game.simulating = not game.simulating
            if event.key == pygame.K_g:
                game.show_grid = not game.show_grid

def update(game):
    if game.simulating:
        game.step_generation()
    else:
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
                game.cells_screen.set_at((x, y), ALIVE_COLOR)
            else:
                game.cells_screen.set_at((x, y), (0, 0, 0, 0))

    # resize play area to window size and display    
    game.window.fill(DEAD_COLOR)
    if game.show_grid:
        game.window.blit(game.grid_screen, (0, 0))
    game.window.blit(pygame.transform.scale(game.cells_screen, WINDOW_SIZE), (0, 0))
    pygame.display.flip()

def main():
    init()
    game = Game()
    # populate cell list based on size of the play area
    for i in range(SCREEN_HEIGHT * SCREEN_WIDTH):
        game.cells.append(CELL_DEAD)

    for x in range(WINDOW_SIZE[0]):
        for y in range(WINDOW_SIZE[1]):
            if x % WINDOW_SCALE != WINDOW_SCALE - 1 and y % WINDOW_SCALE != WINDOW_SCALE - 1:
                game.grid_screen.set_at((x, y), (0, 0, 0, 0))
            else:
                game.grid_screen.set_at((x, y), pygame.Color(ALIVE_COLOR.r, ALIVE_COLOR.g, ALIVE_COLOR.b, 50))

    game.running = True
    
    game.load_layout("default.json")

    while game.running:
        process_input(game)
        update(game)
        render(game)

    pygame.quit()

if __name__ == "__main__":
    main()
