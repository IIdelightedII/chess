from __future__ import annotations
from typing import TYPE_CHECKING

from .constants import *
if TYPE_CHECKING:
    from .board import Board

class Move:
    def __init__(self, move):
        self.__start, self.__end = self.get_index(move)

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @staticmethod
    def get_index(move) ->tuple[ tuple[int, int], tuple[int, int]]:
        if not len(move) == 4:
            raise ValueError(f"ход был неправильно написан: {move}")
        letters_list = []
        for i in range(SIZE):
            letters_list.append(chr(65 + i))
        if not (move[0] in letters_list and move[2] in letters_list):
            raise ValueError(f"ожидалось, что будет написана буква от A до H: {move}")
        if not (move[1].isdigit() and move[3].isdigit()):
            raise TypeError(f"ожидалось, что передадут число: {move}")
        if not (1 <= int(move[1]) <= SIZE and 1 <= int(move[3]) <= SIZE):
            raise ValueError(f"ожидалось, что будет число от 1 до {SIZE}: {move}")
        if move[0:2] == move[2:4]:
            raise ValueError(f"ожидалось, что конечная клетка будет другая: {move}")
        try:
            start = move[0:2]
            start_x = int((ord(start[0]) - 64)) - 1
            start_y = 8 - int(start[1])
            end = move[2:4]
            end_x = int((ord(end[0]) - 64)) - 1
            end_y = 8 - int(end[1])
            return (start_x, start_y), (end_x, end_y)
        except Exception as e:
            raise TypeError(f"ожидалось число: {move}\n{e}")

    def __str__(self):
        return f"{self.__start}, {self.__end}"

    def __repr__(self):
        return self.__str__()




if __name__ == "__main__":
    # print(move("B2B4"))
    pass
