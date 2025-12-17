import socket
import threading
import json
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

with open(os.path.join(
   os.path.dirname(__file__), "info.json"), 'r') as f:
    info = json.load(f)

IP = info["ip"]
PORT = int(info["port"])
REGISTER_STATE = 0
FIND_STATE = 1
GAME_STATE = 2
SIZE = 8
WHITE = "░"
BLACK = "▓"
current_state = None
server_public_key = None
symmetric_key = os.urandom(32)
iv = os.urandom(16)
server_symmetric_key = None
private_key = None
deliver_thread = None


def print_board(matrix):
    print("  ", end="")
    for i in range(SIZE):
        print(chr(65 + i), end=" ")
    print()
    line_num = 8
    for line in matrix:
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


def fill_cells():
    matrix = []
    for i in range(SIZE):
        line = []
        for j in range(SIZE):
            if i % 2 == 0:
                if j % 2 == 0:
                    line.append(WHITE)
                else:
                    line.append(BLACK)
            else:
                if j % 2 == 0:
                    line.append(BLACK)
                else:
                    line.append(WHITE)
        matrix.append(line)
    return matrix



def fill_figures(matrix, fen):
    position = fen.split(" ")[0]
    hoirzontals = position.split("/")
    height = 0
    for line in hoirzontals:
        cell = 0
        for symbol in line:
            if symbol.isdigit():
                cell += int(symbol)
            else:
                matrix[height][cell] = symbol

                cell += 1
        height += 1
    return matrix

    # header_length = int.from_bytes(socket.recv(4), "big")
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

def accept_message(user_socket: socket.socket, private_key):
    global current_state, REGISTER_STATE, GAME_STATE, server_public_key, server_symmetric_key, deliver_thread
    public_key = private_key.public_key()
    print("началось принятие сообщений")
    while True:
        try:
            user_data = original_data(user_socket).decode("utf-8")
            print(user_data)
            user_data = json.loads(user_data)
            if user_data["code"][0] == "0":
                if user_data["code"][1] == "0":
                    print("началась регистрация")
                    current_state = REGISTER_STATE
                if user_data["code"][1] == "1":
                    print("регистрация закончилась")
                    current_state = FIND_STATE
            elif user_data["code"][0] == "1":
                current_state = REGISTER_STATE
                if user_data["code"][1] == "0":
                    print("возникла ошибка: вы ввели не то количество значений через пробел")
                elif user_data["code"][1] == "1":
                    print("возникла ошибка: логин или пароль не введён")
                elif user_data["code"][1] == "2":
                    print("возникла ошибка: введённого логина нет в белом списке")
                elif user_data["code"][1] == "3":
                    print("возникла ошибка: введённого пароля нет в белом списке")
            elif user_data["code"][0] == "2":
                current_state = GAME_STATE
                if user_data["code"][1] == "0":
                    print("вы нашли игру")
            elif user_data["code"][0] == "3":
                    print("доска:")
                    print_board(fill_figures(fill_cells(), user_data["fen"]))
                    print(user_data["fen"])
                    if user_data["code"][1] == "0":
                        print("пришла ваша очередь")
                    elif user_data["code"][1] == "1":
                        print("началась очередь соперника")
                    elif user_data["code"][1] == "2":
                        print("успешный ход")
                    elif user_data["code"][1] == "3":
                        print("неуспешный ход")
            elif user_data["code"][0] == "4":
                current_state = FIND_STATE
                if user_data["code"][1] == "0":
                    print("произошла ошибка со стороны сервера: игра не существует")
                elif user_data["code"][1] == "1":
                    print("игра закончена")
                    print_board(fill_figures(fill_cells(), user_data["fen"]))
            elif user_data["code"][0] == "5":
                current_state = REGISTER_STATE
                if user_data["code"][1] == "0":
                    print("произошли непредвиденные обстоятельства")
            elif user_data["code"][0] == "6":
                if user_data["code"][1] == "0":
                    server_public_key = user_data["key"].encode()
                    print("1")
                    new_public_key = serialization.load_pem_public_key(server_public_key)
                    deliver_thread = threading.Thread(target=deliver_message, args=(user_socket, public_key), daemon=True)
                    deliver_thread.start()
                    print("2")
                elif user_data["code"][1] == "1":
                    send_symmetric_key(user_socket, new_public_key)
                    bytes_list = user_data["key"]
                    text_key = bytes(bytes_list)
                    server_symmetric_key =  private_key.decrypt(text_key, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
            print(user_data["message"])

        except Exception as e:
            import traceback
            print(f"закончена работа: {e}")
            print("Трассировка:")
            traceback.print_exc()  # Покажет ГДЕ именно произошла ошибка
            user_socket.close()
            break
            # print(f"закончена работа: {e}")
            # user_socket.close()
            # break


def send_message(socket: socket.socket, dictionary: dict):
    string = json.dumps(dictionary)
    byte_string = string.encode("utf-8")
    byte_string = len(byte_string).to_bytes(4,"big") + byte_string
    socket.send(byte_string)



def send_symmetric_key(socket: socket.socket, public_key):
    global symmetric_key
    crypted_key = public_key.encrypt(symmetric_key, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))

    numbers = list(crypted_key)
    dictionary = {"code": "31", "key": numbers}
    string = json.dumps(dictionary)
    byte_string = string.encode("utf-8")
    byte_string = len(byte_string).to_bytes(4,"big") + byte_string
    socket.send(byte_string)

def deliver_message(user_socket: socket.socket, public_key):
    text_public_key = public_key.public_bytes(serialization.Encoding.PEM,
                                              serialization.PublicFormat.SubjectPublicKeyInfo)
    send_message(user_socket, {"key": text_public_key.decode("utf-8"), "code": "30"})
    while True:
        message = input()
        try:
            if current_state == REGISTER_STATE:
                login, password = message.split(" ")
                send_message(user_socket, {"login": login, "password": password, "code": "00"})

            elif current_state == FIND_STATE:
                send_message(user_socket, {"opponent": message, "code": "10"})

            elif current_state == GAME_STATE:
                send_message(user_socket, {"move": message, "code": "20"})
            else:
                print("неизвестное состояние")


        except Exception  as e:
            print(f"кажется вы ввели что-то неправильно, попробуйте снова: {e}, вид ошибки: {type(e)}")





def main():
    global symmetric_key
    try:
        user_socket = socket.socket()
        print("началось подключение")
        user_socket.connect((IP, PORT))
        private_key = rsa.generate_private_key(65537, 4096)




        accept_thread = threading.Thread(target=accept_message, args=(user_socket, private_key), daemon=True)
        accept_thread.start()

        while True:
            time.sleep(1)

    except Exception as e:
        print(f"возникла ошибка: {e}")
        return





while True:
    main()
    print("подключение прервалось, подождите несколько секунд")
    time.sleep(5)
    print("повторная попытка подключения")

# print_board(fill_figures(fill_cells(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

