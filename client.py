import threading
import socket
# from client import Client


IP = "127.0.0.1"
PORT = 20352







def accept_message(user_socket: socket.socket):
    print("началось принятие сообщений")
    while True:
        try:
            user_data = user_socket.recv(1024).decode("utf-8")
            print(user_data)
            code, data = user_data.split("/")
            if code == "0":
            # print("принялось сообщение")
                pass
            if code[0] == "1":
                if code[1] == "0":
                    print("возникла ошибка: вы ввели не то количество значений через пробел")
                elif code[1] == "1":
                    print("логин неверно введён")
                elif code[1] == "2":
                    print("пароль введён неверно")
                elif code[1] == "3":
                    print("пароль введён верно")
            print(data)

        except Exception as e:
            print(f"закончена работа: {e}")
            user_socket.close()
            break


def deliver_message(user_socket: socket.socket):
    while True:
        message = input()
        print(message)
        user_socket.send(message.encode("utf-8"))


def start():
    user_socket = socket.socket()
    print("началось подключение")
    user_socket.connect((IP, PORT))


    accept_thread = threading.Thread(target=accept_message, args=(user_socket,))
    accept_thread.start()

    deliver_message(user_socket)


start()

# matrix = chessboard_matrix(8)
# add_pieces(matrix, 8 )
# print_chessboard_with_labels(matrix)
