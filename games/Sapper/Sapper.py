import random
import emojis


class Cell:

    def __init__(self):
        self.__is_mine = False
        self.__number = 0
        self.__is_open = False
        self.__symbol = None

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        if isinstance(value, int) and 0 <= value <= 8:
            self.__number = value
        else:
            raise ValueError("недопустимое значение атрибута")

    @property
    def is_mine(self):
        return self.__is_mine

    @is_mine.setter
    def is_mine(self, value):
        if isinstance(value, bool):
            self.__is_mine = value
        else:
            raise ValueError("недопустимое значение атрибута")

    @property
    def is_open(self):
        return self.__is_open

    @is_open.setter
    def is_open(self, value):
        if isinstance(value, bool):
            self.__is_open = value
        else:
            raise ValueError("недопустимое значение атрибута")

    @property
    def symbol(self):
        return emojis.encode(self.__symbol)

    @symbol.setter
    def symbol(self, symb):
        accepted_symbs = [":one:",
                          ":two:",
                          ":three:",
                          ":four:",
                          ":five:",
                          ":six:",
                          ":seven:",
                          ":eight:",
                          ":nine:",
                          ":boom:",
                          ]
        if not (symb in accepted_symbs):
            raise ValueError("Недопустимый символ!")
        self.__symbol = symb

    def __bool__(self):
        return False if self.is_open else True


class GamePole:

    def __init__(self, n, m, total_mines):
        self.N = n
        self.M = m
        self.total_mines = total_mines
        self.__pole_cells = [[Cell() for _ in range(m)] for _ in range(n)]
        self.__cell_values = [":one:",
                              ":two:",
                              ":three:",
                              ":four:",
                              ":five:",
                              ":six:",
                              ":seven:",
                              ":eight:",
                              ":nine:"]
        GamePoleLogic.init_pole(self)

    @property
    def pole(self):
        return self.__pole_cells

    @property
    def values(self):
        return self.__cell_values

    def __setattr__(self, key, value):
        if key in ("N", "M") and value == 0:
            raise ValueError("Недопустимый размер поля!")
        super.__setattr__(self, key, value)


class GamePoleLogic:

    @staticmethod
    def init_pole(pole_obi):
        k = pole_obi.total_mines
        k0 = 0
        while k0 < k:
            mine_coord = [random.randint(0, (pole_obi.N - 1)) for _ in range(2)]
            if not pole_obi.pole[mine_coord[0]][mine_coord[1]].is_mine:
                pole_obi.pole[mine_coord[0]][mine_coord[1]].is_mine = True
                k0 += 1
            else:
                continue

        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for i in range(0, pole_obi.N):
            for j in range(0, pole_obi.M):
                if not pole_obi.pole[i][j].is_mine:
                    pole_obi.pole[i][j].number = sum(pole_obi.pole[i + i1][j + j1].is_mine for i1, j1 in indx if
                                                     0 <= i + i1 < pole_obi.N and 0 <= j + j1 <
                                                     pole_obi.M)
                    pole_obi.pole[i][j].symbol = pole_obi.values[pole_obi.pole[i][j].number - 1]

    @staticmethod
    def open_cell(pole_obi, coords):
        i, j = coords
        try:
            pole_obi.pole[i - 1][j - 1]
        except IndexError as idx_err:
            print(idx_err)
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        finally:
            if pole_obi.pole[i - 1][j - 1].is_mine:
                pole_obi.pole[i - 1][j - 1].is_open = True
                pole_obi.pole[i - 1][j - 1].symbol = ":boom:"
                GamePoleLogic.show_pole(pole_obi)
                print("Игра окончена!")
                game_over = True
                return game_over
            elif pole_obi.pole[i - 1][j - 1].is_open:
                print("Данная клетка уже открыта")
            else:
                pole_obi.pole[i - 1][j - 1].is_open = True
                GamePoleLogic.show_pole(pole_obi)

    @staticmethod
    def show_pole(pole_obi):
        for i in range(len(pole_obi.pole)):
            for j in range(len(pole_obi.pole[i])):
                print(pole_obi.pole[i][j].symbol if pole_obi.pole[i][j].is_open else
                      emojis.encode(":white_medium_square:"), end=" ")
            print(end="\n")


if __name__ == "__main__":
    pole = GamePole(10, 10, 50)
    GamePoleLogic.show_pole(pole)
    game_over = False
    while not game_over:
        game_over = GamePoleLogic.open_cell(pole, list(map(int, input("Введите координаты клетки: ").split())))
