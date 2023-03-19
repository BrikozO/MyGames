import random
import emojis


class Cell:

    def __init__(self):
        self.__is_mine = False
        self.__number = 0
        self.__is_open = False
        self.symbol = None

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

    def __bool__(self):
        return False if self.is_open else True


class GamePole:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, N, M, total_mines):
        self.N = N
        self.M = M
        self.__pole_cells = [[Cell() for _ in range(M)] for _ in range(N)]
        self._cell_values = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
        self.total_mines = total_mines
        self.__init_pole()

    @property
    def pole(self):
        return self.__pole_cells

    def __init_pole(self):
        k = self.total_mines
        k0 = 0
        while k0 < k:
            mine_coord = [random.randint(0, (self.N - 1)), random.randint(0, (self.M - 1))]
            if not self.pole[mine_coord[0]][mine_coord[1]].is_mine:
                self.pole[mine_coord[0]][mine_coord[1]].is_mine = True
                k0 += 1
            else:
                continue

        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for i in range(0, self.N):
            for j in range(0, self.M):
                if not self.pole[i][j].is_mine:
                    self.pole[i][j].number = sum(self.pole[i + i1][j + j1].is_mine for i1, j1 in indx if
                                                 0 <= i + i1 < self.N and 0 <= j + j1 <
                                                 self.M)
                    self.pole[i][j].symbol = emojis.encode(self._cell_values[self.pole[i][j].number -1])

    def open_cell(self, coords):
        i, j = coords
        game_over = False
        try:
            self.pole[i - 1][j - 1]
        except:
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        finally:
            if self.pole[i - 1][j - 1].is_mine:
                self.pole[i - 1][j - 1].is_open = True
                self.pole[i - 1][j - 1].symbol = emojis.encode(":boom:")
                self.show_pole()
                print("Игра окончена!")
                game_over = True
                return game_over
            elif self.pole[i - 1][j - 1].is_open:
                print("Данная клетка уже открыта")
            else:
                self.pole[i - 1][j - 1].is_open = True
                self.show_pole()

    def show_pole(self):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                print(self.pole[i][j].symbol if self.pole[i][j].is_open else emojis.encode(":white_medium_square:"), end=" ")
            print(end="\n")


pole = GamePole(10, 10, 50)
pole.show_pole()
game_over = None
while game_over is None:
    game_over = pole.open_cell(list(map(int, input("Введите координаты клетки: ").split())))