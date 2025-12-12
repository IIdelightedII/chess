import threading
import os

class Client:
    def __init__(self, socket):
        self._socket = socket
        self._login = None
        self._list = []
        self._input_thread = None
        self._analysis_thread = None
        self._public_key = None
        self._symmetric_key = None
        self._iv = None

    @property
    def socket(self):
        return self._socket

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def public_key(self):
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        self._public_key = value

    @property
    def symmetric_key(self):
        return self._symmetric_key

    @symmetric_key.setter
    def symmetric_key(self, value):
        self._symmetric_key = value

    def start_input_thread(self, user_input):
        self._input_thread = threading.Thread(target=user_input, args=(self,), daemon=True)
        self._input_thread.start()

    def start_analysis_thread(self, analys):
        self._analysis_thread = threading.Thread(target=analys, args=(self,), daemon=True)
        self._analysis_thread.start()

    def add_data(self, data: dict):
        self._list.append(data)

    def return_data(self):
        list = self._list
        self._list = []
        return list


    @property
    def is_full(self):
        return bool(self._list)