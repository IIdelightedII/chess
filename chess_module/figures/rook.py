from __future__ import annotations
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from ..board import Board
    from .. import Cell
from ..move import Move
from .abstractfigure import AbstractFigure
from ..constants import *
from .king import King
import math

class Rook(AbstractFigure):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "r")
        self._name = self._get_name(self._color, self._name)
 # print(figure.name)
        # for direction in figure.direction:
            # print(difference[0], difference[1])
            # print(direction[0], direction[1])
            # print()
            # if  (direction[0] != 0 and difference[0] % direction[0] == 0 or difference[0] == 0) and \
            #     (direction[1] != 0 and difference[1] % direction[1] == 0 or difference[1] == 0):
            #
            #     print("sss")
            #     step = direction
            #     length = int(difference[0] // step[0])
            #     if length > figure.max_length:
            #         continue
            #     is_same_color = False
            #     for i in range(1, length + 1):
            #         cell = self.__matrix[move.start[1] + step[1] * i][move.start[0] + step[0] * i]
            #         if cell.is_full and cell.figure.color == figure.color:
            #             print(f"hhh: {move.start[1] + step[1] * i}, {move.start[0] + step[0] * i}")
            #             print(step[1], step[0])
            #             print(difference[1], difference[0])
            #             is_same_color = True
            #             break
            #     if is_same_color:
            #         continue
            #     print(step, length)
            #     return True


    def can_move(self, board: Board, move: Move) -> bool:
        delta_x = move.end[0] - move.start[0]
        delta_y = move.end[1] - move.start[1]
        if delta_x != 0 and delta_y != 0:
            return False
        step = int(copysign(1, delta_x)), int(copysign(1, delta_y))
        for i in range(1, abs(delta_x + delta_y)):
            # print(step)
            # print(move.start[0] + step[0] * i)
            # print(move.start[1] + step[1] * i)
            cell = board.matrix[move.start[1] + step[1] * i][move.start[0] + step[0] * i]
            # print(cell.is_full)
            if cell.is_full:
                # print("false")
                return False
        return True


    # def can_move_mate(self, board: Board, move: Move, color) -> bool:
    #     delta_x = move.end[0] - move.start[0]
    #     delta_y = move.end[1] - move.start[1]
    #     if delta_x != 0 and delta_y != 0:
    #         return False
    #     step = int(copysign(1, delta_x)), int(copysign(1, delta_y))
    #     for i in range(1, abs(delta_x + delta_y)):
    #         # print(step)
    #         # print(move.start[0] + step[0] * i)
    #         # print(move.start[1] + step[1] * i)
    #         cell = board.matrix[move.start[1] + step[1] * i][move.start[0] + step[0] * i]
    #         # print(cell.is_full)
    #         if cell.is_full and not(cell.figure is King and cell.figure.color == color):
    #             # print("false")
    #             return False
    #     return True

    def where_can_move(self, board: Board, position: Cell) -> list[Cell]:
        x = position.column
        y = position.row
        cells = []
        for i in range(-8, 8):
            for j in range(-8, 8):
                if( not (0 <= x + i <= 7 and 0 <= y + j <= 7)):
                    continue
                try:
                    move = Move(f"{chr(ord("A") + x)}{str(8 - y)}{chr(ord("A")+ x + i)}{str(8 - (y + j))}")
                except:
                    continue
                if board.can_move_no_color(move):
                     cells.append(board.matrix[y + j][x + i])
        return cells



