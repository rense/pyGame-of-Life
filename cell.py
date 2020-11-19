import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from settings import CELL_STATE_DEAD, CELL_STATE_ALIVE, GAME_GRID_COLOR, GAME_CELL_COLOR, GRID_CELL_THICKNESS


class Cell:

    def __init__(self, game, width, height, x, y):
        self.game = game
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.position = Vector2(x * self.width, y * self.height)

        self.surface = Surface((self.width, self.height))
        self.rect = self.surface.get_rect()

        self.neighbours = []

        self.state = CELL_STATE_DEAD
        self.next_state = None

    def kill(self):
        self.state = CELL_STATE_DEAD
        self.next_state = None

    def revive(self):
        self.state = CELL_STATE_ALIVE
        self.next_state = None

    def get_neighbours(self):
        _neighbours = []

        for y in range(-1, 2):
            for x in range(-1, 2):
                if [x, y] == [0, 0]:
                    continue

                _y = self.y - y
                _x = self.x - x
                if _y < 0:
                    _y += self.game.rows
                elif _y > self.game.rows - 1:
                    _y -= self.game.rows
                if _x < 0:
                    _x += self.game.cols
                elif _x > self.game.cols - 1:
                    _x -= self.game.cols

                cell = self.game.grid[_y][_x]

                _neighbours.append(cell)
        return _neighbours

    @property
    def alive_neighbours(self):
        count = 0
        for n in self.neighbours:
            if n.state == CELL_STATE_ALIVE:
                count += 1
        return count

    def toggle(self):
        print(self.state)
        if self.state == CELL_STATE_DEAD:
            self.revive()
        else:
            self.kill()

    def update(self):
        self.rect.topleft = (self.position.x, self.position.y)

    def draw(self):
        self.surface.fill(GAME_GRID_COLOR)

        if self.state == CELL_STATE_ALIVE:
            pygame.draw.rect(
                self.surface,
                GAME_CELL_COLOR,
                (
                    0,
                    0,
                    self.width,
                    self.height
                )
            )
        else:
            pygame.draw.rect(
                self.surface,
                (255, 255, 255),
                (
                    GRID_CELL_THICKNESS,
                    GRID_CELL_THICKNESS,
                    self.width + GRID_CELL_THICKNESS,
                    self.height + GRID_CELL_THICKNESS
                )
            )

        self.game.surface.blit(self.surface, (self.position.x, self.position.y))
