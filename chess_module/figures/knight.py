from __future__ import annotations
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from ..board import Board
    from .. import Cell
    from ..move import Move
from .abstractfigure import AbstractFigure

class Knight(AbstractFigure):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "n")
        self._name = self._get_name(self._color, self._name)

    def can_move(self, board: Board, move: Move) -> bool:
        delta_x = move.end[0] - move.start[0]
        delta_y = move.end[1] - move.start[1]
        if abs(delta_x) not in (1, 2) or abs(delta_y) not in (1, 2) or abs(delta_x) == abs(delta_y):
            return False
        return True

    def where_can_move(self, board: Board, position: Cell) -> set[Cell]:
        x = position.column
        y = position.row
        cells = set()
        for i in range(-2, 3):
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