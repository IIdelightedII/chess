from __future__ import annotations
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from ..board import Board
    from ..move import Move
    from ..cell import Cell
from ..constants import *


class AbstractFigure:
    def __init__(self, color: Literal["w", "b"], name: str):
        self._color = color
        if self._color not in [WHITE, BLACK]:
            raise ValueError("цвет фигуры не черный или белый")
        self._name = name


    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color



    def can_move(self, board: Board, move: Move) -> bool:
        return False


    def where_can_move(self, board: Board, position: Cell) -> tuple[Cell]:
        pass

    @staticmethod
    def _get_name(color, name):
        if color == WHITE:
            return name.upper()
        elif color == BLACK:
            return name.lower()

    def __str__(self):
        return self._name
