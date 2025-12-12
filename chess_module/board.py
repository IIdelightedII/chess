from __future__ import annotations
import math
from .cell import Cell
from .constants import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .move import Move
from .figures import *


class Board:
    def __init__(self, fen: str= "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.__matrix = []
        self.__figures = {"r": Rook, "b": Bishop, "q": Queen, "p": Pawn, "n": Knight, "k": King}
        self.__fill_cells()
        self.__fill_figures(fen)
        self.__color_to_move = WHITE if fen.split(" ")[1] == "w" else BLACK


    @property
    def color_to_move(self):
        return self.__color_to_move

    def make_fen(self):
        addition = " KQkq - 0 1"
        move = " w" if self.__color_to_move == WHITE else " b"
        main = ""
        for line in self.__matrix:
            num = 0
            for cell in line:
                if cell.is_empty:
                    num += 1
                else:
                    if num != 0:
                        main += str(num)
                        main += str(cell)
                        num = 0
                    else:
                        num = 0
                        main += str(cell)
            if num != 0:
                main += str(num)
            main += "/"
        return main[:-1] + move + addition

    @property
    def matrix(self):
        return self.__matrix

    def print_board(self):
        print("  ", end="")
        for i in range(SIZE):
            print(chr(65 + i), end=" ")
        print()
        line_num = 8
        for line in self.__matrix:
            print(f"{line_num}", end=" ")
            for cell in line:
                print(cell, end=" ")
            print(f"{line_num}", end=" ")
            line_num -= 1
            print()
        print("  ", end="")
        for i in range(SIZE):
            print(chr(65 + i), end=" ")
        print()


    def __fill_cells(self):
        for i in range(SIZE):
            line = []
            for j in range(SIZE):
                if i % 2 == 0:
                    if j % 2 == 0:
                        line.append(Cell(WHITE, i, j))
                    else:
                        line.append(Cell(BLACK, i, j))
                else:
                    if j % 2 == 0:
                        line.append(Cell(BLACK, i, j))
                    else:
                        line.append(Cell(WHITE, i, j))
            self.__matrix.append(line)

    def __fill_figures(self, fen):
        position = fen.split(" ")[0]
        hoirzontals = position.split("/")
        height = 0
        for line in hoirzontals:
            cell = 0
            for symbol in line:
                if symbol.isdigit():
                    cell += int(symbol)
                else:
                    self.__matrix[height][cell].figure = self.__figures[symbol.lower()](WHITE if symbol.isupper() else BLACK)
                    cell += 1
            height += 1

    def can_move(self, move: Move) -> bool:
        if self.can_move_no_color(move):
            start_cell = self.__matrix[move.start[1]][move.start[0]]
            figure = start_cell.figure
            if figure.color != self.__color_to_move:
                return False
        else:
            return False
        return True


    def can_move_no_color(self, move: Move):
        start_cell =  self.__matrix[move.start[1]][move.start[0]]
        if start_cell.is_empty:
            return False
        figure = start_cell.figure
        end_cell = self.__matrix[move.end[1]][move.end[0]]
        if end_cell.is_full and figure.color == end_cell.figure.color:
            return False
        if not figure.can_move(self, move):
            return False
        return True


    def move(self, move: Move):
        if not self.can_move(move):
            return
        self.__color_to_move = BLACK if self.__color_to_move == WHITE else WHITE
        start_cell = self.__matrix[move.start[1]][move.start[0]]
        end_cell = self.__matrix[move.end[1]][move.end[0]]
        end_cell.figure = start_cell.figure
        start_cell.figure = None
        king =  None
        for i in range(SIZE):
            for j  in range(SIZE):
                if self.__matrix[j][i].is_full and self.__matrix[j][i].figure.name == "K":
                    king = self.__matrix[j][i]
        if king.figure.where_can_move(self, king):
            return True
        else:
            return False


    def  _is_end(self, color) -> bool:
        king_cell = None
        for i in range(SIZE):
            for j in range(SIZE):
                if self.__matrix[j][i].is_full and type(self.__matrix[j][i].figure) is King and self.__matrix[j][i].figure.color != color:
                    king_cell = self.__matrix[j][i]

        king_moves = king_cell.figure.where_can_move(self, king_cell)
        king_moves.append(king_cell)
        print(king_moves)

        other_figures = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.__matrix[j][i].is_full and self.__matrix[j][i].figure.color == color:
                    other_figures.append(self.__matrix[j][i])

        for new_king_cell in king_moves:
            if king_cell != new_king_cell:
                new_king_cell.figure = king_cell.figure
                king_cell.figure = None
            attacked_cells = []

            for other_cell in other_figures:
                moves = other_cell.figure.where_can_move(self, other_cell)
                attacked_cells += moves
            if king_cell != new_king_cell:
                king_cell.figure = new_king_cell.figure
                new_king_cell.figure = None
            if new_king_cell not in attacked_cells:
                return False
        return True




