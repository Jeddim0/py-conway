import pygame
import random
from scripts.game import Game

# constants

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240
WINDOW_SCALE = 2
WINDOW_SIZE = SCREEN_WIDTH * WINDOW_SCALE, SCREEN_HEIGHT * WINDOW_SCALE

UPDATES_PER_SEC = 30

CELL_ALIVE = 1
CELL_DEAD = 0

ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

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
    ...

def render(game):
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            cell_state = game.return_cell_from_coords(x, y)
            if cell_state == CELL_ALIVE:
                game.screen.set_at((x, y), ALIVE_COLOR)
            else:
                game.screen.set_at((x, y), DEAD_COLOR)

    
    game.window.blit(pygame.transform.scale(game.screen, WINDOW_SIZE), (0, 0))
    pygame.display.flip()

def main():
    init()
    game = Game()
    for i in range(SCREEN_HEIGHT * SCREEN_WIDTH):
        game.cells.append(random.choice((CELL_ALIVE, CELL_DEAD)))
    game.running = True

    while game.running:
        process_input(game)
        update(game)
        render(game)

    pygame.quit()

if __name__ == "__main__":
    main()
