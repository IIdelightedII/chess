import socket
import threading
import time

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from .client import Client
from .game import Game
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import os


with open(os.path.join(os.path.dirname(__file__), "info.json"), 'r') as f:
    info = json.load(f)

IP = info["ip"]
PORT = int(info["port"])
clients = []
games = []
symmetric_key = os.urandom(32)
iv = os.urandom(16)
white_list = {
    "Al": "12",
    "Bob": "23",
    "Cat": "34",
    "Dan": "45",
    "Eve": "56",
    "Fox": "67",
    "Guy": "78",
    "Ian": "89",
    "Joe": "90",
    "Kim": "11"
}

exit_event = threading.Event()

def input_terminal():
    global exit_event, clients
    session = PromptSession()
    with patch_stdout():
        while True:
            text = session.prompt("> ")
            if text == "exit":
                print("started exit")
                for client in clients:
                    send_message(client, {"code": "50", "message": "сервер прервал свою работу"})
                exit_event.set()
                pass
            elif text == "show_all_players":
                print("players:")
                for user in clients:
                    print(user.login)


def send_symmetric_key(client: Client):
    global symmetric_key
    text_public_key = client.public_key.encode("utf-8")
    new_public_key = serialization.load_pem_public_key(text_public_key)
    crypted_key = new_public_key.encrypt(symmetric_key, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

    numbers = list(crypted_key)
    dictionary = {"code": "61", "key": numbers, "message": "был получен симметричный ключ"}
    string = json.dumps(dictionary)
    byte_string = string.encode("utf-8")
    byte_string = len(byte_string).to_bytes(4,"big") + byte_string
    client.socket.send(byte_string)

def send_message(client: Client, message: dict):
    string = json.dumps(message)
    byte_string = string.encode("utf-8")
    byte_string = len(byte_string).to_bytes(4, "big") + byte_string
    client.socket.send(byte_string)



def analysis_data(client: Client):
    global white_list, clients, games, exit_event
    print("начат анализ данных")
    while True:
        if exit_event.is_set():
            break
        try:
            if not client.is_full:
                time.sleep(1)
                continue
            print("данные были получены")
            for data in client.return_data():
                print(data["code"])
                if data["code"][0] == "0":
                    login = data["login"]
                    password = data["password"]
                    if not login and password:
                        send_message(client, {"code": "11", "message": "напишите логин и пароль"})
                    elif not login in white_list.keys():
                        send_message(client, {"code": "12", "message": "попробуйте сверится с белым списком"})
                    elif not password == white_list[login]:
                        send_message(client, {"code": "13", "message": "попробуйте сверится с белым списком"})
                    else:
                        print("регистрация окончена")
                        client.login = login
                        send_message(client, {"code": "01", "message": "вы успешно зарегистрировались"})
                elif data["code"] == "10":
                    print(clients)
                    other_client = None
                    for new_client in clients:
                        print("None other?", new_client is None)
                        print("None main?", client is None)
                        if new_client.login == data["opponent"]:
                            other_client = new_client
                    game = Game(client, other_client)
                    games.append(game)
                    send_message(client, {"code": "20", "message": "сейчас вы начнёте игру"})
                    send_message(other_client, {"code": "20", "message": "сейчас вы начнёте игру"})
                    send_message(client, {"code": "30", "message": "ваш ход", "fen": game.fen})
                    send_message(other_client, {"code": "31", "message": "ожидайте ход соперника", "fen": game.fen})
                elif data["code"][0] == "2":
                    if data["code"][1] == "0":

                        current_game = None
                        for game in games:
                            if game.client1 == client or game.client2 == client:
                               current_game = game
                        # print("fen: ", current_game.fen)
                        message = data["move"]
                        current_game.is_end(current_game.client1)
                        if current_game is not None and current_game.is_right_color(client) and current_game.can_move(message):
                            current_game.do_move(message)
                            if current_game.client1 == client:
                                send_message(current_game.client1, {"code": "32", "message": "вы сходили", "fen": current_game.fen})
                                if current_game.is_end(current_game.client1):
                                    send_message(current_game.client1,{"code": "41", "message": "попробуйте найти новую игру", "fen": current_game.fen})
                                    send_message(current_game.client2,{"code": "41", "message": "попробуйте найти новую игру", "fen": current_game.fen})
                                    games.remove(current_game)
                                else:
                                    send_message(current_game.client2, {"code": "30", "message": "ваш ход", "fen": current_game.fen})
                            else:
                                send_message(current_game.client2, {"code": "32", "message": "вы сходили", "fen": current_game.fen})
                                if current_game.is_end(current_game.client2):
                                    send_message(current_game.client1,{"code": "41", "message": "попробуйте найти новую игру", "fen": current_game.fen})
                                    send_message(current_game.client2,{"code": "41", "message": "попробуйте найти новую игру", "fen": current_game.fen})
                                    games.remove(current_game)
                                else:
                                    send_message(current_game.client1, {"code": "30", "message": "ваш ход", "fen": current_game.fen})
                        else:
                            if current_game is None:
                                send_message(client, {"code": "40", "message": "попробуйте пересоздать игру или зайти к кому-то другому"})
                            else:
                                send_message(client, {"code": "33", "message": "вы неправильно сходили или не должны были ходить", "fen": current_game.fen})
                elif data["code"][0] == "3":
                    if data["code"][1] == "0":
                        public_key = data["key"]
                        client.public_key = public_key
                        print(type(client.public_key))
                        send_symmetric_key(client)
                    elif data["code"][1] == "1":
                        client.symmetric_key = data["key"]
                        send_message(client, {"code": "00",
                                              "message": "начните регистрацию, напишите логин и пароль через пробел"})
        except Exception as e:
            print(f"произошла ошибка: {e}")

def get_information(socket: socket.socket, header_length: int):
    bytes_info = b""
    bytes_left = header_length
    while bytes_left > 0:
        new_info = socket.recv(bytes_left)
        bytes_left -= len(new_info)
        bytes_info += new_info
    return bytes_info

def original_data(socket: socket.socket):
    message_length = int.from_bytes(get_information(socket, 4), "big")
    return get_information(socket, message_length)

def user_input(client: Client):
    global clients, exit_event
    client.socket.settimeout(0.5)
    while True:
        if exit_event.is_set():
            break
        try:
            user_data = original_data(client.socket).decode("utf-8")
            client.add_data(json.loads(user_data))
        except socket.timeout:
            continue
        except Exception as e:
            clients.remove(client)
            print(f"пользователь закончил сеанс: {e}")
            break




def main():
    global symmetric_key
    print(IP)
    terminal_thread = threading.Thread(target=input_terminal, daemon=True)
    terminal_thread.start()
    print("1")
    try:
        server_socket = socket.socket()
        print("2")
        server_socket.bind((IP, PORT))
        print("3")
        private_key = rsa.generate_private_key(65537, 4096)
        public_key = private_key.public_key()
        print(public_key)
        server_socket.listen()
    except Exception as e:
        print(f"ошибка: {e}")
        return


    while True:
        try:
            if exit_event.is_set():
                break
            data = server_socket.accept()
            client = Client(data[0])
            client.socket.settimeout(0.5)
            text_public_key = public_key.public_bytes(serialization.Encoding.PEM,
                                                      serialization.PublicFormat.SubjectPublicKeyInfo)
            print(text_public_key)


            clients.append(client)
            print("подключился пользователь")

            client.start_input_thread(user_input)
            client.start_analysis_thread(analysis_data)
            send_message(client, {"code": "60", "key": text_public_key.decode("utf-8"), "message": "был получен ключ"})
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
    print("Done")





# def start():
#     global exit_event
#     main_thread = threading.Thread(target=main, daemon=True)
#     main_thread.start()
#     while True:
#         if exit_event.is_set():
#             print("Done")
#             break
# d

main()
