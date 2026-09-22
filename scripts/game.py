import pygame

class Game:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if not hasattr(self, 'cells'):
            self.cells = []

    def return_cell_from_coords(self, x, y):
        screen_size = list(self.screen.size)
        screen_width = screen_size[0]

        idx = y * screen_width + x
        return self.cells[idx]
