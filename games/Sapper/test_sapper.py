import emojis
import pytest

from Sapper import Cell, GamePoleLogic, GamePole


def test_symbol_assigment_encode_in_cell():
    g = Cell()
    g.symbol = ":boom:"
    assert g.symbol == emojis.encode(":boom:"), "Неправильно отработало присваивание символа клетке!"


def test_symbol_assigment_in_cell():
    g = Cell()
    with pytest.raises(ValueError):
        g.symbol = 1


@pytest.mark.parametrize("a, b", [(0, 1),
                                  ("string", 10),
                                  (10, "string"),
                                  (10, 55)])
def test_input_data_in_pole(a, b):
    with pytest.raises(ValueError):
        GamePole(a, b)


