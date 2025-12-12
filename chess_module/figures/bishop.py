from __future__ import annotations
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from ..board import Board
    from chess_module.cell import Cell
    from ..move import Move
from .abstractfigure import AbstractFigure
from ..constants import *
import math


class Bishop(AbstractFigure):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "b")
        self._name = self._get_name(self._color, self._name)


    def can_move(self, board: Board, move: Move) -> bool:
        delta_x = move.end[0] - move.start[0]
        delta_y = move.end[1] - move.start[1]
        if abs(delta_x) != abs(delta_y):
            return False
        step = int(copysign(1, delta_x)), int(copysign(1, delta_y))
        is_same_color = False
        for i in range(1, abs(delta_x)):
            cell = board.matrix[move.start[1] + step[1] * i][move.start[0] + step[0] * i]
            if cell.is_full:
                is_same_color = True
                break
        if is_same_color:
            return False
        else:
            return True


    def where_can_move(self, board: Board, position: Cell) -> set[Cell]:
        x = position.column
        y = position.row
        cells = set()
        for i in range(-8, 8):
            for j in range(-8, 8):
                if not (0 <= x + i <= 7 and 0 <= y + j <= 7):
                    continue
                try:
                    move = Move(f"{chr(ord("A") + x)}{str(8 - y)}{chr(ord("A")+ x + i)}{str(8 - (y + j))}")
                except:
                    continue
                if board.can_move_no_color(move):
                     cells.add(board.matrix[y + j][x + i])
        return cells