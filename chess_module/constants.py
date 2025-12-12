SIZE = 8
WHITE = "░"
BLACK = "▓"
def copysign(number: float | int, sign_to_copy: float | int):
    if sign_to_copy > 0:
        return number
    elif sign_to_copy < 0:
        return -number
    else:
        return 0


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