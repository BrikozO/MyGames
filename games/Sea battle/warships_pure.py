import random
import time
from random import randint
import emojis


class Ship:

    def __init__(self, length, tp=1, x=None, y=None, size=10, ):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._size = size
        self._cells = {}
        self.indx = None

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __getitem__(self, item):
        return self._cells[item]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y
        if self.is_out_pole():
            raise ValueError()

    def get_start_coords(self) -> tuple:
        return self._x, self._y

    def calc_position(self) -> tuple:
        if self._tp == 1:
            self.indx = [(i, j) for j in range(self._x, self._x + self._length) for i in
                         range(self._y, self._y + 1)]
        else:
            self.indx = [(i, j) for i in range(self._y, self._y + self._length) for j in
                         range(self._x, self._x + 1)]
        for elem in range(self._length):
            self._cells[self.indx[elem]] = 1
        return self.indx, self._cells

    def is_collide(self, ship) -> bool:
        if ship._tp == 1:
            indx_ship = [(i, j) if (0 <= i <= ship._size - 1 and 0 <= j <= ship._size - 1) else None for j in
                         range(ship._x - 1, ship._x + ship._length + 1) for i in
                         range(ship._y - 1, ship._y + 2)]
        else:
            indx_ship = [(i, j) if (0 <= i <= ship._size - 1 and 0 <= j <= ship._size - 1) else None for i in
                         range(ship._y - 1, ship._y + ship._length + 1) for j in
                         range(ship._x - 1, ship._x + 2)]
        result = [x for x in self.indx for y in indx_ship if x is not None and y == x]
        return False if len(result) == 0 else True

    def is_out_pole(self, size=10):
        if not (0 <= self._x <= size) or not (0 <= self._y <= size):
            return True
        else:
            if (self._tp == 1 and self._x + self._length > size) or (
                    self._tp == 2 and self._y + self._length > size):
                return True
        return False


class GamePole:

    def __init__(self, size):
        self._size = size
        self.pole = [[emojis.encode(":droplet:") for _ in range(size)] for _ in range(size)]
        self._ships = []

    def init(self):
        self._ships = [Ship(4, size=self._size, tp=randint(1, 2)),
                       Ship(3, size=self._size, tp=randint(1, 2)),
                       Ship(3, size=self._size, tp=randint(1, 2)),
                       Ship(2, size=self._size, tp=randint(1, 2)),
                       Ship(2, size=self._size, tp=randint(1, 2)),
                       Ship(2, size=self._size, tp=randint(1, 2)),
                       Ship(1, size=self._size, tp=randint(1, 2)),
                       Ship(1, size=self._size, tp=randint(1, 2)),
                       Ship(1, size=self._size, tp=randint(1, 2)),
                       Ship(1, size=self._size, tp=randint(1, 2))]
        ships_placed = []
        for index, ship in enumerate(self._ships):
            not_placed = True
            while not_placed:
                ship._x = randint(0, self._size - 1)
                ship._y = randint(0, self._size - 1)
                if ship.is_out_pole():
                    continue
                else:
                    ship.calc_position()
                    collided = False
                    for shp in ships_placed:
                        if shp.is_collide(ship):
                            collided = True
                        else:
                            pass
                    if not collided:
                        ships_placed.append(ship)
                        not_placed = False
                    else:
                        ship._cells = {}
                        continue

    def get_ships(self) -> list:
        return self._ships

    def show(self, is_user=False):
        for ship in self._ships:
            for idx in ship.indx:
                if not is_user:
                    self.pole[idx[0]][idx[1]] = [ship, emojis.encode(":droplet:")] if ship._cells[idx] == 1 else [
                    ship, emojis.encode(":skull:")]
                else:
                    self.pole[idx[0]][idx[1]] = [ship, emojis.encode(":ship:")] if ship._cells[idx] == 1 else [
                    ship, emojis.encode(":skull:")]
        for string in self.pole:
            string = [symb if type(symb) != list else symb[1] for symb in string]
            print(*string)

    def get_pole(self) -> list:
        return self.pole


class GameLogic:

    def __init__(self):
        self.user_field = GamePole(10)
        self.user_field.init()
        print("Ваше игровое поле:")
        self.user_field.show(is_user=True)
        self.bot_field = GamePole(10)
        self.bot_field.init()
        self.already_hitted_user = []
        self.already_hitted_bot = []
        self.user_dead = 0
        self.bot_dead = 0

    def shoot_logic(self, field: list, crd1: int, crd2: int) -> GamePole.show:
        ship = field.pole[crd1 - 1][crd2 - 1][0]
        if not isinstance(ship, Ship):
            field.pole[crd1 - 1][crd2 - 1] = emojis.encode(":fire:")
            print("Промах!")
        else:
            ship._cells[(crd1 - 1, crd2 - 1)] = 0
            collection_cells = [val for val in ship._cells.values()]
            if field == self.bot_field:
                if len(list(set(collection_cells))) == 1:
                    print(f"{ship._length}-палубный корабль потоплен!")
                    self.bot_dead += 1
                    if self.bot_dead == 10:
                        game_over = True
                        print("Поздравляем, вы победили!")
                        return game_over
                else:
                    print("Попадание!")
            else:
                if len(list(set(collection_cells))) == 1:
                    print(f"Ваш {ship._length}-палубный корабль потоплен!")
                    self.user_dead += 1
                    if self.user_dead == 10:
                        game_over = True
                        print("Вы проиграли!")
                        return game_over
                else:
                    print("Попадание по вам!")
        field.show(is_user=True if field == self.user_field else False)

    def __call__(self, *args, **kwargs):
        user_move, crd1, crd2 = args
        if user_move:
            for coords in self.already_hitted_user:
                if coords[0] == crd1 and coords[1] == crd2:
                    print("Вы уже били в эту точку!")
                    break
            self.already_hitted_user.append([crd1, crd2])
            self.shoot_logic(self.bot_field, crd1, crd2)
        else:
            dont_shoot = True
            while dont_shoot:
                for coords in self.already_hitted_bot:
                    if coords[0] == crd1 and coords[1] == crd2:
                        crd1 = random.randint(1, 10)
                        crd2 = random.randint(1, 10)
                        break
                self.already_hitted_bot.append([crd1, crd2])
                dont_shoot = False
            self.shoot_logic(self.user_field, crd1, crd2)


game = GameLogic()
k = 0
game_over = None
while game_over is None:
    user_move = True
    x, y = map(int, input("Введите коориданты точки: ").split())
    game_over = game(user_move, x, y)
    user_move = False
    print("Бот делает ход...")
    time.sleep(random.randint(1, 3))
    game(user_move, random.randint(1, 10), random.randint(1, 10))
    k = k + 1
