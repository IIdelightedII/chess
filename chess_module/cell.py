from typing import Literal
from .constants import *
from .figures import AbstractFigure

class Cell:
    def __init__(self, color: Literal["w", "b"], row, column):
        self.__color = color
        self.__row = row
        self.__column = column
        self.__figure = None

    @property
    def figure(self):
        return self.__figure

    @figure.setter
    def figure(self, value: AbstractFigure | None):
        if not isinstance(value, AbstractFigure) and value != None:
            raise TypeError("В клетку можно присваивать только фигуру ")
        self.__figure = value

    @property
    def color(self):
        return self.__color

    @property
    def is_empty(self) -> bool:
        return self.__figure == None

    @property
    def is_full(self) -> bool:
        return self.__figure != None

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

    def __str__(self):
        # return f"{chr(ord("A") + self.__column)}{8 - self.__row}"
        if self.is_full:
            return str(self.__figure)
        if self.__color == WHITE:
            return "░"
        elif self.__color == BLACK:
            return "▓"

    def __repr__(self):
        return self.__str__()

