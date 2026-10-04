import pygame
import json 
import numpy as np
from scipy.signal import convolve2d

CELL_ALIVE = 1
CELL_DEAD = 0

class Game:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if not hasattr(self, 'cells'):
            self.cells = []

    def save_layout(self, file="layout.json"):
        with open(file, "w") as fp:
            json.dump(self.cells, fp)

    def load_layout(self, file="layout.json"):
        with open(file, "r") as fp:
            new_layout = json.load(fp)
            if len(new_layout) == len(self.cells):
                self.cells = new_layout

    def step_generation(self):
        screen_size = list(self.cells_screen.size)
        screen_width = screen_size[0]
        screen_height = screen_size[1]

        grid = np.array(self.cells, dtype=np.uint8).reshape(screen_height, screen_width)
        kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
        neighbors = convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)
        new_grid = ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(np.uint8)
        self.cells = new_grid.flatten().tolist()


    # def determine_possible_neigbours(self, cell_idx):
        # neighbours_absolute = []
        # neighbours_relative = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
# 
        # cell_coords = self.coords_from_idx(cell_idx)
        # 
        # for neighbour in neighbours_relative:
            # neighbours_absolute.append(((cell_coords[0] + neighbour[0]), (cell_coords[1] + neighbour[1])))
# 
        # return neighbours_absolute
        # 
# 
    # def get_new_state(self, cell_idx):
        # living_neighbours = 0
        # neighbours = self.determine_possible_neigbours(cell_idx)
        # for neighbour in neighbours:
            # try:
                # neighbour_value = self.return_cell_from_coords(neighbour[0], neighbour[1])
                # if neighbour_value == CELL_ALIVE:
                    # living_neighbours += 1
            # except IndexError:
                # # this is if we try and access off screen cells anyway so no issue 
                # pass
# 
        # if self.cells[cell_idx] == CELL_DEAD and living_neighbours == 3:
             # return CELL_ALIVE
        # elif self.cells[cell_idx] == CELL_ALIVE and living_neighbours != 2 and living_neighbours != 3:
            # return CELL_DEAD
        # 
        # x, y = self.coords_from_idx(cell_idx)   
        # return self.return_cell_from_coords(x, y)
    
    def coords_from_idx(self, idx):
        screen_size = list(self.cells_screen.size)
        screen_width = screen_size[0]

        y = idx // screen_width
        x = idx % screen_width 

        return x, y

    def return_cell_from_coords(self, x, y):
        screen_size = list(self.cells_screen.size)
        screen_width = screen_size[0]

        idx = y * screen_width + x
        return self.cells[idx]

    def set_cell_at_coords(self, x, y, new_state):
        screen_size = list(self.cells_screen.size)
        screen_width = screen_size[0]

        idx = y * screen_width + x

        try:
            self.cells[idx] = new_state 
        except IndexError: # if we try to change a cell that would be off screen if it existed, we can just pass
            pass
