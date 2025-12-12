from chess_module import Board
from server_module.server.client import Client
from chess_module.constants import *
from chess_module.move import Move


class Game:
    def __init__(self, client1: Client, client2: Client):
        self._client1 = client1
        self._client2 = client2
        self._board = Board()


    @property
    def fen(self):
         return self._board.make_fen()

    @property
    def client1(self):
        return self._client1

    @property
    def client2(self):
        return self._client2

    def can_move(self, message: str):
        try:
            move = Move(message)
        except Exception as e:
            print(f"ошибка: {e}")
            return False
        if self._board.can_move(move):
            return True
        return False

    def is_right_color(self, client: Client) -> bool:
        if self._board.color_to_move == WHITE and client == self._client1:
            return True
        elif self._board.color_to_move == BLACK and client == self._client2:
            return True
        return False


    def do_move(self, move: str):
        move = Move(move)
        self._board.move(move)

    def is_end(self, client) -> bool:
        color = WHITE if client == self._client1 else BLACK
        return self._board._is_end(color)

