import emojis
import pytest

from Sapper import Cell, GamePoleLogic, GamePole


def test_zero_pole():
    with pytest.raises(ValueError):
        GamePole(0, 1, 20)


def test_symbol_in_cell():
    g = Cell()
    g.symbol = ":boom:"
    assert g.symbol == emojis.encode(":boom:"), "Неверное присваивание символа клетке!"
    with pytest.raises(ValueError):
        g.symbol = 1
