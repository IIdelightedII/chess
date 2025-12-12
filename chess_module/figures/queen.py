from __future__ import annotations
from typing import Literal, TYPE_CHECKING

# from .. import Cell

if TYPE_CHECKING:
    from ..board import Board
    from ..move import Move
from .abstractfigure import AbstractFigure
from .bishop import Bishop
from.rook import Rook

class Queen(Rook, Bishop):
    def __init__(self, color: Literal["w", "b"]):
        AbstractFigure.__init__(self, color, "q")
        self._name = self._get_name(self._color, self._name)

    def can_move(self, board: Board, move: Move) -> bool:
        return Rook.can_move(self, board, move) or Bishop.can_move(self, board, move)

