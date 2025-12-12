from __future__ import annotations
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from ..board import Board
    from .. import Cell
from ..move import Move
from .abstractfigure import AbstractFigure
from ..constants import *

class Pawn(AbstractFigure):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "p")
        self._name = self._get_name(self._color, self._name)


    def can_move(self, board: Board, move: Move) -> bool:
        if self.color == BLACK:
            can_move_two_tiles = move.start[1] == 1
            delta_x = move.end[0] - move.start[0]
            delta_y = move.end[1] - move.start[1]


            end_cell = board.matrix[move.end[1]][move.end[0]]
            if delta_y < 1:
                return False
            if delta_y >= 3:
                return False
            if abs(delta_x) > 1:
                return False
            if delta_y == 2:
                if not can_move_two_tiles:
                    return False
                if delta_x != 0:
                    return False
            if abs(delta_x) == 1:
                if not end_cell.is_full:
                    return False

            return True
        else:
            can_move_two_tiles = move.start[1] == 6
            delta_x = move.end[0] - move.start[0]
            delta_y = move.end[1] - move.start[1]


            end_cell = board.matrix[move.end[1]][move.end[0]]
            if delta_y >= 0:
                return False
            if delta_y <= -3:
                return False
            if abs(delta_x) > 1:
                return False
            if delta_y == -2:
                if not can_move_two_tiles:
                    return False
                if delta_x != 0:
                    return False
            if abs(delta_x) == 1:
                if not end_cell.is_full:
                    return False

            return True

    def where_can_move(self, board: Board, position: Cell) -> set[Cell]:
        x = position.column
        y = position.row
        cells = set()
        for i in range(-1, 2):
            for j in range(-2, 3):
                if not (0 <= x + i <= 7 and 0 <= y + j <= 7):
                    continue
                try:
                    move = Move(f"{chr(ord("A") + x)}{str(8 - y)}{chr(ord("A")+ x + i)}{str(8 - (y + j))}")
                except:
                    continue
                if board.can_move_no_color(move):
                    cells.add(board.matrix[y + j][x + i])
        return cells