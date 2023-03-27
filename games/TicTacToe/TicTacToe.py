import random
import time


class TicTacToe:
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2

    def __init__(self):
        self.init()
        self.is_human_win = False
        self.is_computer_win = False
        self.is_draw = False

    def __check_cycle(self, lst):
        for line in lst:
            if all((line[0] == "x", line[1] == "x", line[2] == "x")):
                self.is_human_win = True
                break
            elif all((line[0] == "o", line[1] == "o", line[2] == "o")):
                self.is_computer_win = True
                break

    def __check_combinations(self):
        checkrows = [[self.pole[1 - 1][j].symbol, self.pole[1][j].symbol, self.pole[1 + 1][j].symbol] for j in
                     range(3)]
        checkcols = [[self.pole[i][j].symbol for j in range(3)] for i in range(3)]
        checkdiag1 = [[self.pole[i][i].symbol for i in range(3)]]
        checkdiag2 = [[self.pole[-i-1][i].symbol for i in range(-3, 0)]]
        self.__check_cycle(checkrows)
        self.__check_cycle(checkcols)
        self.__check_cycle(checkdiag1)
        self.__check_cycle(checkdiag2)
        if not self.is_human_win and not self.is_computer_win:
            k = 0
            for line in self.pole:
                for elem in line:
                    if elem.symbol in ["o", "x"]:
                        k = k + 1
            if k == 9:
                self.is_draw = True

    def __check_index(self, indx):
        try:
            self.pole[indx[0]][indx[1]]
        except:
            raise IndexError('некорректно указанные индексы')

    def replace_elem(self, elem, value):
        if elem.is_free:
            elem.value = value
            if value == 1:
                elem.symbol = "x"
            elif value == 2:
                elem.symbol = "o"
            elem.is_free = False
        else:
            raise ValueError('клетка уже занята')

    def init(self):
        self.pole = [[Cell() for _ in range(3)] for _ in range(3)]
        self.is_human_win = False
        self.is_computer_win = False
        self.is_draw = False

    def show(self):
        for string in self.pole:
            for elem in string:
                print(elem.symbol, end=" ")
            print(end="\n")

    def human_go(self):
        coords = [int(x) - 1 for x in input("Введите координаты постановки крестика: ").split()]
        i, j = coords
        if not (0 <= i <= 2) or not (0 <= j <= 2):
            raise ValueError("Некорректные координаты")
        self.__check_index(coords)
        self.replace_elem(self.pole[i][j], self.HUMAN_X)
        self.__check_combinations()

    def computer_go(self):
        is_placed = False
        while not is_placed:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if self.pole[i][j].value == 0:
                self.replace_elem(self.pole[i][j], self.COMPUTER_O)
                is_placed = True
                self.__check_combinations()
            else:
                continue

    def __setitem__(self, key, value):
        self.__check_index(key)
        i, j = key
        self.replace_elem(self.pole[i][j], value)
        self.__check_combinations()

    def __getitem__(self, item):
        self.__check_index(item)
        r, c = item
        return self.pole[r][c].value

    def __bool__(self):
        if not self.is_human_win and not self.is_computer_win and not self.is_draw:
            return True
        else:
            return False


class Cell:

    def __init__(self):
        self.is_free = True
        self.value = 0
        self.symbol = "-"

    def __bool__(self):
        return True if self.value == 0 else False


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")