import random


class Agent:
    def __init__(self, board):
        self.board = board

    def random_play(self):
        """Play a random move"""
        if self.board.game_over:
            return None
        player = self.board.next_player
        player_pieces = [piece for piece in self.board.pieces if piece.player == player]
        all_locations = [(i, j) for i in range(3) for j in range(3)]

        random.shuffle(player_pieces)
        random.shuffle(all_locations)
        for piece in player_pieces:
            for location in all_locations:
                try:
                    self.board.validate_move(piece, location)
                    self.board.play(player, piece.size, piece.index, location)
                except ValueError:
                    continue

    def check_winning_move(self):
        if self.board.game_over:
            return False
        player = self.board.next_player
        player_pieces = [piece for piece in self.board.pieces if piece.player == player]

        for line_indices, visible, actual in self.board.iter_lines():
            if visible.count(player) != 2:
                continue
            for index, gob in zip(line_indices, actual):
                if len(gob) == 0 or gob[0].player != player:
                    possible_winning_location = index
                    for piece in player_pieces:
                        try:
                            if (
                                piece.location != None
                                and piece.location in line_indices
                            ):
                                continue
                            self.board.validate_move(piece, possible_winning_location)
                            self.board.play(
                                player,
                                piece.size,
                                piece.index,
                                possible_winning_location,
                            )
                            return True
                        except ValueError:
                            continue
        return False

    def defend(self):
        if self.board.game_over:
            return None
        player = self.board.next_player
        player_pieces = [piece for piece in self.board.pieces if piece.player == player]
        opponent = "X" if player == "O" else "O"

        for line_indices, visible, actual in self.board.iter_lines():
            if visible.count(opponent) != 2:
                continue
            for index in line_indices:
                for piece in player_pieces:
                    try:
                        self.board.validate_move(piece, index)
                        self.board.play(
                            player,
                            piece.size,
                            piece.index,
                            index,
                        )
                        if self.check_winning_move():
                            self.board.undo(2)
                            continue
                        return True
                    except ValueError:
                        continue
        return False

    def prefer_new(self):
        if self.board.game_over:
            return None
        player = self.board.next_player
        player_pieces = [piece for piece in self.board.pieces if piece.player == player]
        new_pieces = [piece for piece in player_pieces if piece.location == None]
        all_locations = [(i, j) for i in range(3) for j in range(3)]

        random.shuffle(new_pieces)
        random.shuffle(all_locations)
        for piece in new_pieces:
            for location in all_locations:
                try:
                    self.board.validate_move(piece, location)
                    self.board.play(player, piece.size, piece.index, location)
                    return True
                except ValueError:
                    continue
        return False

    def play(self):
        """Helper function for a normal strategy
        1. Check if game is over
        2. Try to play a winning move
        3. If can't win, try to defend
        4. If can't defend, play a random move
        """

        if self.board.game_over:
            return

        won = self.check_winning_move()
        if won:
            return

        defended = self.defend()
        if not defended:
            self.prefer_new()

    def play_out(self):
        for _ in range(50):
            self.play()
