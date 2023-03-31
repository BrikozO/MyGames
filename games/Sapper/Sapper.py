import random
import emojis


class Cell:
    """
    Представление клетки
    """

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
        return self.__symbol

    @symbol.setter
    def symbol(self, symb):
        accepted_symbs = [":zero:",
                          ":one:",
                          ":two:",
                          ":three:",
                          ":four:",
                          ":five:",
                          ":six:",
                          ":seven:",
                          ":eight:",
                          ":nine:",
                          ":boom:",
                          ":triangular_flag_on_post:"
                          ]
        if not (symb in accepted_symbs):
            raise ValueError("Недопустимый символ!")
        self.__symbol = emojis.encode(symb)

    def __bool__(self):
        return True if self.is_open else False


class GamePole:
    """
    Представление игрового поля
    """

    def __init__(self, columns_rows: int, mines_percent: int) -> None:
        self.columns_rows = columns_rows
        self.mines_percent = mines_percent
        self.__pole_cells = [[Cell() for _ in range(self.columns_rows)] for _ in range(self.columns_rows)]
        self.__cell_values = [":zero:",
                              ":one:",
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
        if key in ("columns_rows", "mines_percent") and not isinstance(value, int):
            raise ValueError(f"Недопустимое значение {key} - {type(value)}")
        if key in ("columns_rows", "mines_percent") and value == 0:
            raise ValueError(f"Недопустимое количество {key}")
        if key == "mines_percent" and value > 50:
            raise ValueError(f"Слишком большой процент мин! ({value})")
        super.__setattr__(self, key, value)


class GamePoleLogic:
    """
    Представление логики игрового поля
    """

    # Инициализация игрового поля
    @staticmethod
    def init_pole(pole_obj: GamePole):
        k = int((pole_obj.columns_rows ** 2 / 100) * pole_obj.mines_percent)
        print(k)
        k0 = 0
        while k0 < k:
            mine_coord = [random.randint(0, (pole_obj.columns_rows - 1)) for _ in range(2)]
            if not pole_obj.pole[mine_coord[0]][mine_coord[1]].is_mine:
                pole_obj.pole[mine_coord[0]][mine_coord[1]].is_mine = True
                k0 += 1
            else:
                continue

        indx = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for i in range(0, pole_obj.columns_rows):
            for j in range(0, pole_obj.columns_rows):
                if not pole_obj.pole[i][j].is_mine:
                    pole_obj.pole[i][j].number = sum(pole_obj.pole[i + i1][j + j1].is_mine for i1, j1 in indx
                                                     if 0 <= i + i1 < pole_obj.columns_rows
                                                     and 0 <= j + j1 < pole_obj.columns_rows)
                    pole_obj.pole[i][j].symbol = pole_obj.values[pole_obj.pole[i][j].number]

    # Проверка координат клетки
    @staticmethod
    def check_coords(columns_rows: int, coords: list) -> list:
        i, j = coords
        if not (0 < i <= columns_rows + 1 and 0 < j <= columns_rows):
            raise IndexError('Некорректные индексы i, j клетки игрового поля')
        return [i, j]

    # Открытие клетки на поле
    @staticmethod
    def open_cell(pole_obj: GamePole, coords: list) -> (bool, None):
        i, j = GamePoleLogic.check_coords(pole_obj.columns_rows, coords)
        if pole_obj.pole[i - 1][j - 1].symbol == ":triangular_flag_on_post:":
            raise KeyError('В данную клетку установлен флаг!')
        elif pole_obj.pole[i - 1][j - 1].is_mine:
            pole_obj.pole[i - 1][j - 1].is_open = True
            pole_obj.pole[i - 1][j - 1].symbol = ":boom:"
            GamePoleLogic.show_pole(pole_obj)
            print('Игра окончена!')
            end = True
            return end
        elif pole_obj.pole[i - 1][j - 1].is_open:
            raise KeyError('Данная клетка уже открыта')
        else:
            pole_obj.pole[i - 1][j - 1].is_open = True
            GamePoleLogic.show_pole(pole_obj)

    # Установка флага в клетку с преподолагаемой миной
    @staticmethod
    def set_mine_flag(pole_obj: GamePole, coords: list):
        i, j = GamePoleLogic.check_coords(pole_obj.columns_rows, coords)
        if pole_obj.pole[i - 1][j - 1].is_open:
            print('Вы не можете установить флаг в открытую клетку')
        else:
            pole_obj.pole[i - 1][j - 1].is_open = True
            pole_obj.pole[i - 1][j - 1].symbol = ":triangular_flag_on_post:"
            GamePoleLogic.show_pole(pole_obj)

    # Отображение всего поля
    @staticmethod
    def show_pole(pole_obj: GamePole):
        for i in range(len(pole_obj.pole)):
            for j in range(len(pole_obj.pole[i])):
                print(pole_obj.pole[i][j].symbol if bool(pole_obj.pole[i][j]) else
                      emojis.encode(":white_medium_square:"), end=" ")
            print(end="\n")


if __name__ == "__main__":

    def command_handler(command: str, pole: GamePole) -> (bool, None):
        try:
            coords = list(map(int, input("Введите координаты клетки: ").split()))
        except ValueError:
            print("Некорректные входные данные - координаты клетки должны быть числами!")
        else:
            if command == "Открыть клетку":
                ending = GamePoleLogic.open_cell(pole, coords)
                return ending
            else:
                GamePoleLogic.set_mine_flag(pole, coords)


    pole = GamePole(10, 30)
    GamePoleLogic.show_pole(pole)
    game_over = False
    while not game_over:
        cmd = input("Что вы хотите сделать? (Открыть клетку/Установить флаг): ")
        if cmd == "Открыть клетку":
            try:
                game_over = command_handler(cmd, pole)
            except Exception as exc:
                print(exc)
                game_over = command_handler(cmd, pole)
        elif cmd == "Установить флаг":
            try:
                command_handler(cmd, pole)
            except Exception as exc:
                print(exc)
                command_handler(cmd, pole)
        else:
            raise TypeError("Неизвестная команда!")
