from gobblers.board import Board, Gobbler
import pytest


def test_init_board():
    """When I create a board:
    1. state is a 3x3 array of None
    2. next_player is 'X'
    3. game_over is False
    4. moves is an empty list
    """
    board = Board()
    assert board.state == [[[], [], []], [[], [], []], [[], [], []]]
    assert board.next_player == "X"
    assert board.game_over == False
    assert board.moves == []


def test_init_board_pieces():
    """When I create a board:
    1. there is a pieces list
    2. the pieces list contains 2 gobblers of each size for each player
    """
    board = Board()
    assert len(board.pieces) == 12

    for player in ["X", "O"]:
        for size in [1, 2, 3]:
            for index in [0, 1]:
                gobbler = board.find(player, size, index)
                assert gobbler.player == player
                assert gobbler.size == size
                assert gobbler.index == index


def test_init_gobbler():
    """When I create a gobbler:
    1. the input arg size is 1, 2, or 3
    2. the input arg player is 'X' or 'O'
    3. the index is 0 or 1
    4. the string method shows an arrangement of X or O of the correct size in a 3x3 grid
    5. covered is False
    """
    gobbler = Gobbler("X", 1, 0)
    assert gobbler.size == 1
    assert gobbler.player == "X"
    assert gobbler.index == 0
    assert str(gobbler) == "    X    "
    assert gobbler.covered == False

    gobbler = Gobbler("O", 2, 0)
    assert gobbler.size == 2
    assert gobbler.player == "O"
    assert gobbler.index == 0
    assert str(gobbler) == "    OO OO"
    assert gobbler.covered == False

    gobbler = Gobbler("X", 3, 1)
    assert gobbler.size == 3
    assert gobbler.player == "X"
    assert gobbler.index == 1
    assert str(gobbler) == "XXXXXXXXX"
    assert gobbler.covered == False

    with pytest.raises(ValueError) as e:
        Gobbler("X", 4, 0)
    assert str(e.value) == "Size must be 1, 2, or 3"

    with pytest.raises(ValueError) as e:
        Gobbler("Z", 1, 1)
    assert str(e.value) == "Player must be 'X' or 'O'"

    with pytest.raises(ValueError) as e:
        Gobbler("X", 1, 2)
    assert str(e.value) == "Index must be 0 or 1"


def test_play():
    """When I play a move:
    1. the move is added to the moves list
    2. the next_player is updated
    3. the state is updated with the move
    4. the location is updated on the gobbler that was played
    """
    board = Board()
    board.play("X0", (0, 0))

    assert board.moves == ["X0-0-0"]
    assert board.next_player == "O"
    gobbler = board.find("X", 1, 0)
    assert board.state[0][0] == [gobbler]
    assert gobbler.location == (0, 0)

    board.play("OO1", (1, 0))
    assert board.moves == ["X0-0-0", "OO1-1-0"]
    assert board.next_player == "X"
    gobbler = board.find("O", 2, 1)
    assert board.state[1][0] == [gobbler]

    board.play("XXX0", (2, 2))
    assert board.moves == ["X0-0-0", "OO1-1-0", "XXX0-2-2"]
    assert board.next_player == "O"
    gobbler = board.find("X", 3, 0)
    assert board.state[2][2] == [gobbler]


def test_validate():
    """When I play a move:
    1. it must be my turn
    2. I can go on top if my pice is a strictly larger size
    """
    board = Board()

    with pytest.raises(ValueError) as e:
        board.play("X0", (-1, 0))
    assert str(e.value) == "Location must be a tuple of 2 integers between 0 and 2"

    with pytest.raises(ValueError) as e:
        board.play("X0", (0, 3))
    assert str(e.value) == "Location must be a tuple of 2 integers between 0 and 2"

    with pytest.raises(ValueError) as e:
        board.play("OO1", (0, 0))
    assert str(e.value) == "It is not O's turn"

    board.play("X0", (0, 0))
    with pytest.raises(ValueError) as e:
        board.play("O1", (0, 0))
    assert str(e.value) == "0-0 is occupied by a gobbler of the same size"

    board.play("OO1", (0, 0))
    assert board.moves == ["X0-0-0", "OO1-0-0"]


def test_covering():
    """When a piece is covered
    1. it remains in the state at that location
    2. the covered attribute is True
    3. it is not allowed to move

    When a piece is uncovered
    1. it remains in the state at that location
    2. the covered attribute is False
    3. it is allowed to move
    """

    board = Board()
    board.play("X0", (0, 0))
    first_gobbler = board.find("X", 1, 0)
    board.play("OO1", (0, 0))
    second_gobbler = board.find("O", 2, 1)

    assert board.state[0][0] == [second_gobbler, first_gobbler]
    assert first_gobbler.covered == True

    with pytest.raises(ValueError) as e:
        board.play("X0", (1, 1))
    assert str(e.value) == "This gobbler is covered and cannot move"

    ## burn a move so that it is O's turn
    board.play("X1", (1, 1))

    board.play("OO1", (1, 1))

    assert board.state[0][0] == [first_gobbler]
    assert first_gobbler.covered == False

    board.play("X0", (2, 0))
    assert first_gobbler.location == (2, 0)


def test_print():
    """The string method prints the board
    1. each position on the 3x3 board appears as a 3x3 grid
    2. for each element of state, we show the gobbler in position 0
    """
    board = Board()
    board.play("X0", (0, 0))
    board.play("OO0", (0, 0))
    board.play("XXX0", (1, 1))
    board.play("O1", (0, 2))
    board.play("XXX1", (0, 1))

    output = board.print()

    expected_output = ""
    expected_output += "   |XXX|   \n"
    expected_output += " OO|XXX| O \n"
    expected_output += " OO|XXX|   \n"
    expected_output += "---+---+---\n"
    expected_output += "   |XXX|   \n"
    expected_output += "   |XXX|   \n"
    expected_output += "   |XXX|   \n"
    expected_output += "---+---+---\n"
    expected_output += "   |   |   \n"
    expected_output += "   |   |   \n"
    expected_output += "   |   |   \n"

    assert output == expected_output


def test_win():
    pass
