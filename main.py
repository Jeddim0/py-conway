# MIT License
# Copyright (c) 2026 Jeddim0


import pygame
import random
import numpy as np
from scripts.game import Game

# constants

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 160, 120
WINDOW_SCALE = 8
WINDOW_SIZE = SCREEN_WIDTH * WINDOW_SCALE, SCREEN_HEIGHT * WINDOW_SCALE

UPDATES_PER_SEC = 30

CELL_ALIVE = 1
CELL_DEAD = 0

ALIVE_COLOR = pygame.Color('white')
DEAD_COLOR  = pygame.Color('black')
COLORKEY = DEAD_COLOR

# tuple forms for numpy broadcasting
ALIVE_RGBA = tuple(ALIVE_COLOR)          # (255, 255, 255, 255)
DEAD_RGBA  = (0, 0, 0, 0)                # transparent

# init and game loop functions

def init():
    pygame.init()
    game = Game()
    game.grid_screen = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    game.cells_screen = pygame.Surface(SCREEN_SIZE)
    game.cells_screen.set_colorkey(COLORKEY)
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
                if event.key == pygame.K_c:
                    game.cells = [0 for cell in game.cells]
            if event.key == pygame.K_SPACE:
                game.simulating = not game.simulating
            if event.key == pygame.K_g:
                game.show_grid = not game.show_grid

def update(game):
    if game.simulating:
        game.step_generation()
    # else:
    m_pos = pygame.mouse.get_pos()
    
    # convert mouse pos in window to play area coords
    m_pos = (m_pos[0] // WINDOW_SCALE, m_pos[1] // WINDOW_SCALE)
    m_buttons = pygame.mouse.get_pressed()

    if m_buttons[0]:
        game.set_cell_at_coords(m_pos[0], m_pos[1], CELL_ALIVE)

    if m_buttons[2]:
        game.set_cell_at_coords(m_pos[0], m_pos[1], CELL_DEAD)

def render(game):
    game.window.fill(DEAD_COLOR)
    cells = np.array(game.cells, dtype=np.uint8).reshape(SCREEN_HEIGHT, SCREEN_WIDTH).T

    arr = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT, 3), dtype=np.uint8)
    arr[..., 0] = np.where(cells == CELL_ALIVE, 255, 0)   # R
    arr[..., 1] = np.where(cells == CELL_ALIVE, 255, 0)   # G
    arr[..., 2] = np.where(cells == CELL_ALIVE, 255, 0)   # B
    # arr[..., 3] = np.where(cells == CELL_ALIVE, 255, 0)   # A

    pygame.surfarray.blit_array(game.cells_screen, arr)
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

        game.clock.tick(40)

    pygame.quit()

if __name__ == "__main__":
    main()
