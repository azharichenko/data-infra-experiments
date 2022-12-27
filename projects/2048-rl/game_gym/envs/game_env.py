import gym
from gym import spaces
from gym import utils
from gym.utils import seeding, EzPickle
import numpy as np

from enum import Enum, IntEnum
from random import randint, choice
from typing import Tuple


class Action(IntEnum):
    UP: int = 0
    DOWN: int = 1
    LEFT: int = 2
    RIGHT: int = 3


class GameBoard:
    def __init__(self):
        self.board_matrix = [0] * 16
        self.score = 0
        self.generate_random_piece()
        self.generate_random_piece()
        self.action_func_mapping = {
            Action.DOWN: self.merge_down,
            Action.UP: self.merge_up,
            Action.RIGHT: self.merge_right,
            Action.LEFT: self.merge_left,
        }

    def perform_action(self, action: Action) -> int:
        score_movement, moved = self.action_func_mapping[action]()
        if moved:
            self.generate_random_piece()

        if score_movement:
            return 1
        return -1

    def _loc_value(self, row, col):
        return self.board_matrix[(row * 4) + col]

    def _loc_calc(self, row, col):
        return (row * 4) + col

    def merge_left(self) -> Tuple[bool, bool]:
        score_increase, has_moved = False, False
        for col in range(1, 4):
            for row in range(4):
                empty_cell = self._loc_value(row, col) == 0

                if empty_cell:
                    continue

                col_cur = col
                for new_col in reversed(range(0, col)):
                    if self._loc_value(row, new_col) == 0:
                        self.board_matrix[self._loc_calc(row, new_col)] = self._loc_value(row, col_cur)
                        self.board_matrix[self._loc_calc(row, col_cur)] = 0
                        has_moved = True
                    elif self._loc_value(row, col_cur) == self._loc_value(row, new_col):
                        self.board_matrix[self._loc_calc(row, new_col)] *= 2
                        self.board_matrix[self._loc_calc(row, col_cur)] = 0
                        has_moved = True
                        score_increase = True
                        break
                    else:
                        break
                    col_cur = new_col

        return score_increase, has_moved
    def merge_right(self) -> Tuple[bool, bool]:
        score_increase, has_moved = False, False
        for col in reversed(range(3)):
            for row in range(4):
                empty_cell = self._loc_value(row, col) == 0

                if empty_cell:
                    continue

                col_cur = col
                for new_col in range(col + 1, 4):
                    if self._loc_value(row, new_col) == 0:
                        self.board_matrix[self._loc_calc(row, new_col)] = self._loc_value(row, col_cur)
                        self.board_matrix[self._loc_calc(row, col_cur)] = 0
                        has_moved = True
                    elif self._loc_value(row, col_cur) == self._loc_value(row, new_col):
                        self.board_matrix[self._loc_calc(row, new_col)] *= 2
                        self.board_matrix[self._loc_calc(row, col_cur)] = 0
                        has_moved = True
                        score_increase = True
                        break
                    else:
                        break
                    col_cur = new_col

        return score_increase, has_moved

    def merge_down(self) -> Tuple[bool, bool]:
        score_increase, has_moved = False, False
        for row in reversed(range(3)):
            for col in range(4):
                empty_cell = self._loc_value(row, col) == 0

                if empty_cell:
                    continue

                row_cur = row
                for new_row in range(row + 1, 4):
                    if self._loc_value(new_row, col) == 0:
                        self.board_matrix[self._loc_calc(new_row, col)] = self._loc_value(row_cur, col)
                        self.board_matrix[self._loc_calc(row_cur, col)] = 0
                        has_moved = True
                    elif self._loc_value(row_cur, col) == self._loc_value(new_row, col):
                        self.board_matrix[self._loc_calc(new_row, col)] *= 2
                        self.board_matrix[self._loc_calc(row_cur, col)] = 0
                        has_moved = True
                        score_increase = True
                        break
                    else:
                        break
                    row_cur = new_row

        return score_increase, has_moved

    def merge_up(self) -> Tuple[bool, bool]:
        score_increase, has_moved = False, False
        for row in range(1, 4):
            for col in range(4):
                empty_cell = self._loc_value(row, col) == 0

                if empty_cell:
                    continue

                row_cur = row
                for new_row in reversed(range(0, row)):
                    if self._loc_value(new_row, col) == 0:
                        self.board_matrix[self._loc_calc(new_row, col)] = self._loc_value(row_cur, col)
                        self.board_matrix[self._loc_calc(row_cur, col)] = 0
                        has_moved = True
                    elif self._loc_value(row_cur, col) == self._loc_value(new_row, col):
                        self.board_matrix[self._loc_calc(new_row, col)] *= 2
                        self.board_matrix[self._loc_calc(row_cur, col)] = 0
                        has_moved = True
                        score_increase = True
                        break
                    else:
                        break
                    row_cur = new_row

        return score_increase, has_moved

    def generate_random_piece(self) -> None:
        piece: int = np.random.choice(a=[2, 4], p=[0.9, 0.1])
        r, c = randint(0, 3), randint(0, 3)

        while self.board_matrix[(r * 4) + c] != 0:
            r, c = randint(0, 3), randint(0, 3)

        self.board_matrix[(r * 4) + c] = piece

    def print_board(self):
        for i in range(4):
            print(self.board_matrix[i * 4 : (i * 4) + 4])
        print()

    def is_done(self):
        if any(v == 0 for v in self.board_matrix):
            return False
        return True


class GameEnv(gym.Env, EzPickle):
    metadata = {"render.modes": ["human"]}

    def __init__(self, *args, **kwargs):
        # Actions | 0: Up, 1: Down, 2: Left, 3: Right
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(16)

        self.board = GameBoard()

    def reset(self):
        self.board = GameBoard()

    def step(self, action):
        reward = self.board.perform_action(action)
        done = self.board.is_done()
        return self.board.board_matrix, reward, done, {}

    def render(self, mode="human"):
        print("#" * 20)
        self.board.print_board()


if __name__ == "__main__":
    game = GameBoard()
    game.print_board()
    for _ in range(3):
        print(_, "#" * 80)
        game.perform_action(action=Action.LEFT)
        game.print_board()
        # game.perform_action(action=Action.UP)
        # game.print_board()
