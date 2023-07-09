from typing import Any


class Board:
    def __init__(self):
        self.state = [[[] for _ in range(3)] for _ in range(3)]
        self.next_player = "X"
        self.game_over = False
        self.moves = []
        self._init_pieces()

    def _init_pieces(self):
        self.pieces = []
        for player in ["X", "O"]:
            for size in [1, 2, 3]:
                self.pieces.append(Gobbler(player, size, 0))
                self.pieces.append(Gobbler(player, size, 1))

    def _parse_move(self, move):
        if move[-1] not in ["0", "1"]:
            raise ValueError("Move must end index 0 or 1")
        if move[0] not in ["X", "O"]:
            raise ValueError("Move must start with player 'X' or 'O'")
        return self.find(move[0], len(move[:-1]), int(move[-1]))

    def validate_move(self, gobbler, location):
        if gobbler.player != self.next_player:
            raise ValueError("It is not {}'s turn".format(gobbler.player))

        if len(location) != 2:
            raise ValueError("Location must be a tupple of 2 integers between 0 and 2")

        if gobbler.covered:
            raise ValueError("This gobbler is covered and cannot move")

        x, y = location
        if x not in [0, 1, 2] or y not in [0, 1, 2]:
            raise ValueError("Location must be a tuple of 2 integers between 0 and 2")

        if len(self.state[x][y]) > 0:
            existing_gobbler = self.state[x][y][0]
            can_eat = gobbler.can_eat(existing_gobbler)
            if not can_eat:
                raise ValueError(
                    "{}-{} is occupied by a gobbler of the same size".format(x, y)
                )

    def find(self, player, size, index):
        for piece in self.pieces:
            if piece.player == player and piece.size == size and piece.index == index:
                return piece
        raise ValueError("No piece found", player, size, index)

    def _check_cover_and_uncover(self, gobbler, location):
        x, y = location
        if len(self.state[x][y]) > 0:
            self.state[x][y][0].covered = True
        if gobbler.location is None:
            return

        x, y = gobbler.location
        self.state[x][y].remove(gobbler)
        if len(self.state[x][y]) > 0:
            self.state[x][y][0].covered = False

    def play(self, move, location):
        gobbler = self._parse_move(move)
        self.validate_move(gobbler, location)
        move_string = "{}-{}-{}".format(move, location[0], location[1])
        self.moves.append(move_string)
        self.next_player = "X" if self.next_player == "O" else "O"
        x, y = location

        self._check_cover_and_uncover(gobbler, location)

        self.state[x][y].insert(0, gobbler)
        gobbler.location = location

    def print(self):
        """
        example output
           |   |
         X |   |
           |   |
        ---+---+---
           |OOO|
           |OOO|
           |OOO|
        ---+---+---
           |   |
         XX|   | OO
         XX|   | OO
        """
        output = ""

        strings = [["" for _ in range(3)] for _ in range(3)]
        for i, row in enumerate(self.state):
            for j, gobblers in enumerate(row):
                if len(gobblers) == 0:
                    strings[i][j] = "         "
                else:
                    strings[i][j] = str(gobblers[0]).replace("\n", "")

        for row in strings:
            for i in range(3):
                output += (
                    "{}|{}|{}".format(
                        row[0][3 * i : 3 * (i + 1)],
                        row[1][3 * i : 3 * (i + 1)],
                        row[2][3 * i : 3 * (i + 1)],
                    )
                    + "\n"
                )
            if row != strings[-1]:
                output += "---+---+---\n"
        return output


class Gobbler:
    def __init__(self, player, size, index):
        if size not in [1, 2, 3]:
            raise ValueError("Size must be 1, 2, or 3")
        if player not in ["X", "O"]:
            raise ValueError("Player must be 'X' or 'O'")
        if index not in [0, 1]:
            raise ValueError("Index must be 0 or 1")

        self.size = size
        self.player = player
        self.index = index
        self.location = None
        self.covered = False

    def can_eat(self, other):
        return self.size > other.size

    def __str__(self):
        if self.size == 1:
            return "    {}    ".format(self.player)
        elif self.size == 2:
            return "    {} {}".format(self.player * 2, self.player * 2)

        elif self.size == 3:
            return "{}{}{}".format(self.player * 3, self.player * 3, self.player * 3)

    def __eq__(self, other):
        print(self.location, other.location)
        return (
            self.size == other.size
            and self.player == other.player
            and self.index == other.index
            and self.location == other.location
        )
