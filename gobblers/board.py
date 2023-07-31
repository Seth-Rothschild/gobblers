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

    def _parse_move(self, player, size, index):
        if player not in ["X", "O"]:
            raise ValueError("Move must start with player 'X' or 'O'")
        if size not in [1, 2, 3]:
            raise ValueError("Move must end with size 1, 2, or 3")
        if index not in [0, 1]:
            raise ValueError("Move must end index 0 or 1")
        return self.find(player, size, index)

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

    def _get_visible_gobblers(self):
        visible = [[None for _ in range(3)] for _ in range(3)]
        for i, row in enumerate(self.state):
            for j, gobblers in enumerate(row):
                if len(gobblers) > 0:
                    visible[i][j] = gobblers[0].player
        return visible

    def _check_win(self):
        visible = self._get_visible_gobblers()
        rows = visible
        columns = [[row[i] for row in visible] for i in range(3)]
        diagonals = [
            [visible[0][0], visible[1][1], visible[2][2]],
            [visible[0][2], visible[1][1], visible[2][0]],
        ]

        for line in rows + columns + diagonals:
            if line[0] is not None and line[0] == line[1] == line[2]:
                return True
        return False

    def find(self, player, size, index):
        for piece in self.pieces:
            if piece.player == player and piece.size == size and piece.index == index:
                return piece
        raise ValueError("No piece found", player, size, index)

    def validate_move(self, gobbler, location):
        if gobbler.player != self.next_player:
            raise ValueError("It is not {}'s turn".format(gobbler.player))

        if len(location) != 2:
            raise ValueError("Location must be a tupple of 2 integers between 0 and 2")

        if gobbler.covered:
            raise ValueError("This gobbler is covered and cannot move")

        if self.game_over:
            raise ValueError("The game is over")

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

        # check if the move reveals three in a row by _check_win with piece removed
        if gobbler.location is None:
            return
        x, y = gobbler.location
        self.state[x][y].remove(gobbler)
        is_valid = not self._check_win()
        self.state[x][y].insert(0, gobbler)
        if not is_valid:
            raise ValueError("This move reveals three in a row")

    def undo(self, number_of_moves=1):
        moves = self.moves
        for _ in range(number_of_moves):
            moves.pop()
        self.__init__()
        self.replay(moves)

    def play(self, player, size, index, location):
        gobbler = self._parse_move(player, size, index)
        self.validate_move(gobbler, location)
        move_string = "{}-{}-{}-{}-{}".format(
            player, size, index, location[0], location[1]
        )
        self.moves.append(move_string)
        self.next_player = "X" if self.next_player == "O" else "O"
        x, y = location

        self._check_cover_and_uncover(gobbler, location)

        self.state[x][y].insert(0, gobbler)
        if self._check_win():
            self.game_over = True
            self.winner = gobbler.player
        gobbler.location = location

    def _reflect_move(self, move, type):
        player, size, index, x, y = move.split("-")
        if type == 0:
            x = str(2 - int(x))
        if type == 1:
            x, y = y, x
        if type == 2:
            y = str(2 - int(y))
        if type == 3:
            x = str(2 - int(x))
            y = str(2 - int(y))
            x, y = y, x
        return "-".join([player, size, index, x, y])

    def reflect(self, type):
        if type not in [0, 1, 2, 3]:
            raise ValueError("Reflection arg must be 0, 1, 2, or 3")
        new_moves = [self._reflect_move(move, type) for move in self.moves]

        self.replay(new_moves)

    def replay(self, moves):
        self.__init__()
        for move in moves:
            player, size, index, x, y = move.split("-")
            self.play(player, int(size), int(index), (int(x), int(y)))

    def iter_lines(self):
        """Go through the rows and columns and give useful information about them"""

        indices = [[(i, j) for j in range(3)] for i in range(3)]
        column_indices = [[(i, j) for i in range(3)] for j in range(3)]
        diagonals = [
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]

        visible = self._get_visible_gobblers()
        column_visible = [[row[i] for row in visible] for i in range(3)]
        diagonal_visible = [
            [visible[0][0], visible[1][1], visible[2][2]],
            [visible[0][2], visible[1][1], visible[2][0]],
        ]

        actual = self.state
        column_actual = [[row[i] for row in actual] for i in range(3)]
        diagonal_actual = [
            [actual[0][0], actual[1][1], actual[2][2]],
            [actual[0][2], actual[1][1], actual[2][0]],
        ]

        line_indices = indices + column_indices + diagonals
        line_visible = visible + column_visible + diagonal_visible
        line_actual = actual + column_actual + diagonal_actual

        for index, visible, actual in zip(line_indices, line_visible, line_actual):
            yield (index, visible, actual)

    def __str__(self):
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

        self.player = player
        self.size = size
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
        return (
            self.player == other.player
            and self.size == other.size
            and self.index == other.index
            and self.location == other.location
        )
