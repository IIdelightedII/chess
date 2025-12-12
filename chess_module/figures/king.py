from __future__ import annotations
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from ..board import Board

    from ..cell import Cell
from .abstractfigure import AbstractFigure
from ..move import Move

class King(AbstractFigure):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "k")
        self._name = self._get_name(self._color, self._name)


    def can_move(self, board: Board, move: Move) -> bool:
        delta_x = move.end[0] - move.start[0]
        delta_y = move.end[1] - move.start[1]
        if abs(delta_x) > 1 or abs(delta_y) > 1:
            return False
        return True

    def where_can_move(self, board: Board, position: Cell) -> list[Cell]:
        x = position.column
        y = position.row
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (0 <= x + i <= 7 and 0 <= y + j <= 7):
                    continue
                try:
                    move = Move(f"{chr(ord("A") + x)}{str(8 - y)}{chr(ord("A")+ x + i)}{str(8 - (y + j))}")
                except:
                    continue
                if board.can_move_no_color(move):
                     cells.append(board.matrix[y + j][x + i])
        return cells

