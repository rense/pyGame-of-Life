from pygame.math import Vector2
from pygame.surface import Surface

from cell import Cell
from settings import CELL_STATE_ALIVE, CELL_STATE_DEAD
from templates import *


class Game:

    def __init__(self, window, width, height, rows, cols, x, y):
        self.window = window
        self.position = Vector2(x, y)

        self.surface = Surface((width, height))
        self.rect = self.surface.get_rect()

        self.tick = 0

        self.cols = cols
        self.rows = rows
        self.window_width = width
        self.window_height = height
        self.cell_w = self.window_width / self.cols
        self.cell_h = self.window_height / self.rows

        self.grid = self.make_grid()
        for row in self.grid:
            for cell in row:
                cell.neighbours = cell.get_neighbours()

    def make_grid(self):
        grid = [
            [Cell(self, self.cell_w, self.cell_h, x, y) for x in range(self.cols)] for y in range(self.rows)
        ]
        if TEMPLATE is not None:
            for offset in TEMPLATE_OFFSETS:
                print(offset)
                for y, row in enumerate(TEMPLATE):
                    for x, state in enumerate(row):
                        try:
                            grid[y + offset[0]][x + offset[1]].state = state
                        except IndexError:
                            pass
        return grid

    def update(self):
        self.rect.topleft = self.position
        for row in self.grid:
            for cell in row:
                cell.update()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
        self.window.blit(self.surface, (self.position.x, self.position.y))

    def evaluate(self):
        self.tick += 1
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.state == CELL_STATE_ALIVE:
                    if cell.alive_neighbours < 2 or cell.alive_neighbours > 3:
                        cell.next_state = CELL_STATE_DEAD
                    elif cell.alive_neighbours in [2, 3]:
                        cell.next_state = CELL_STATE_ALIVE
                elif cell.alive_neighbours == 3:
                    cell.next_state = CELL_STATE_ALIVE
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.next_state == CELL_STATE_ALIVE:
                    cell.revive()
                if cell.next_state == CELL_STATE_DEAD:
                    cell.kill()
