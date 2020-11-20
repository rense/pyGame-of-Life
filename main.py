import sys

import pygame
from pygame.time import Clock

from game import Game
from settings import (
    CELL_STATE_ALIVE,
    GAME_WIDTH,
    GAME_HEIGHT,
    GAME_BACKGROUND_COLOR,
    GAME_ROWS,
    GAME_COLS,
    GAME_STATE_CONFIG,
    GAME_STATE_QUIT,
    GAME_STATE_RUNNING,
    GAME_FPS,
    GAME_STATE_PAUSED,
    GAME_STATES,
    CELL_WIDTH,
    CELL_HEIGHT,
    GAME_SPEED,
    GAME_TITLE,
    GAME_MAX_SPEED,
    GAME_MIN_SPEED
)


class GameOfLife:

    def start(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        icon = pygame.image.load('assets/gol_icon.png')
        pygame.display.set_icon(icon)

        self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.window.fill(GAME_BACKGROUND_COLOR)

        self.is_fullscreen = False

        self.clock = Clock()
        self.speed = GAME_SPEED

        self.game = Game(
            self.window,
            GAME_WIDTH,
            GAME_HEIGHT,
            GAME_ROWS,
            GAME_COLS,
            0, 0
        )

        self.frame_count = 0
        self.state = GAME_STATE_CONFIG
        self.main()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GAME_STATE_QUIT
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and self.state != GAME_STATE_RUNNING:
                cursor_position = pygame.mouse.get_pos()
                if self.cursor_on_grid(cursor_position):
                    self.click_cell(cursor_position)
                    continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_q:
                self.state = GAME_STATE_QUIT

            if event.key == pygame.K_SPACE:
                self.set_state()
            if event.key == pygame.K_ESCAPE:
                self.reset_state()
            if event.key == pygame.K_PRINTSCREEN:
                self.print_grid()

            if event.key == pygame.K_KP_PLUS:
                self.speed = min(GAME_MAX_SPEED, self.speed + 1)
                print(f"speed {self.speed}")

            if event.key == pygame.K_KP_MINUS:
                self.speed = max(GAME_MIN_SPEED, self.speed - 1)
                print(f"speed {self.speed}")

            if event.key == pygame.K_f:
                if self.window.get_flags() & pygame.FULLSCREEN:
                    self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
                else:
                    self.window = pygame.display.set_mode(
                        (GAME_WIDTH, GAME_HEIGHT),
                        pygame.FULLSCREEN
                    )

    def main(self):
        while self.state != GAME_STATE_QUIT:
            self.frame_count += 1
            self.get_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(GAME_FPS)

        pygame.quit()
        sys.exit()

    def update(self):
        self.game.update()
        if self.state == GAME_STATE_RUNNING:
            if self.frame_count % (GAME_FPS // self.speed) == 0:
                self.game.evaluate()
                self.set_title()

    def draw(self):
        self.game.draw()

    def set_title(self):
        tick = f" - tick {self.game.tick}" if self.game.tick > 0 else ""
        pygame.display.set_caption(f"{GAME_TITLE}{tick}")

    def set_state(self):
        if self.state == GAME_STATE_CONFIG:
            self.state = GAME_STATE_RUNNING
        elif self.state == GAME_STATE_RUNNING:
            self.state = GAME_STATE_PAUSED
        elif self.state == GAME_STATE_PAUSED:
            self.state = GAME_STATE_RUNNING
        print(GAME_STATES[self.state])

    def reset_state(self):
        if self.state == GAME_STATE_CONFIG:
            return
        self.state = GAME_STATE_CONFIG
        self.game.tick = 0
        self.game.make_grid()
        self.set_title()
        print(GAME_STATES[self.state])

    def cursor_on_grid(self, pos):
        return pos[0] > 0 and pos[0] < GAME_WIDTH and pos[1] > 0 and pos[1] < GAME_HEIGHT

    def click_cell(self, pos):
        grid_pos = [
            int(pos[0] // CELL_WIDTH),
            int(pos[1] // CELL_HEIGHT)
        ]
        cell = self.game.grid[grid_pos[1]][grid_pos[0]]

        cell.toggle()

    def print_grid(self):
        output = []
        for row in self.game.grid:
            _row = []
            for cell in row:
                if cell.state == CELL_STATE_ALIVE:
                    _row.append(1)
                else:
                    _row.append(0)
            output.append(_row)
        print(output)


if __name__ == "__main__":
    GameOfLife().start()
