from gobblers.agent import Agent
from gobblers.board import Board

import pytest


def test_random_play():
    """When I initialize a board and an agent
    I can play valid random moves until the game ends
    The game should end in fewer than 50 moves
    """
    board = Board()
    agent = Agent(board)
    for _ in range(50):
        agent.random_play()
        if board.game_over:
            break
    assert board.game_over == True


def test_check_for_winning_move():
    """When I initialize a board and an agent
    If there is a winning move, agent.check_winning_move() should return true
    agent.play_winning_move() should end the game
    """

    board = Board()
    agent = Agent(board)
    board.play("X", 1, 0, (0, 0))
    board.play("O", 1, 0, (1, 0))
    assert agent.check_winning_move() == False
    board.play("X", 1, 1, (0, 1))
    board.play("O", 1, 1, (1, 1))

    assert agent.check_winning_move() == True
    assert board.game_over == True


def test_game_duration():
    """When I play games trying to win I should finish them faster
    than when I play random moves
    """
    random_moves = []
    for i in range(10):
        board = Board()
        agent = Agent(board)
        for _ in range(50):
            agent.random_play()
            if board.game_over:
                break
        random_moves.append(len(board.moves))

    winning_moves = []
    for i in range(10):
        board = Board()
        agent = Agent(board)
        for _ in range(50):
            won = agent.check_winning_move()
            if not won:
                agent.random_play()
            if board.game_over:
                break
        winning_moves.append(len(board.moves))

    assert sum(random_moves) > sum(winning_moves)


def test_defend():
    """When I defend I should block the opponent's winning move"""
    board = Board()
    agent = Agent(board)
    board.play("X", 1, 0, (0, 0))
    board.play("O", 1, 0, (1, 0))
    board.play("X", 1, 1, (0, 1))
    # Defend as O
    assert agent.defend()

    # X should not be able to win on the next move
    assert agent.check_winning_move() == False


def test_edge_cases():
    """Regression test for previously broken cases
    These are games where O moves a piece to enable an X win

    Given the choice, we will not play moves that reveal 2-in-a-row
    """

    bad_games = [
        ["X-1-0-1-1", "O-3-0-1-1", "X-3-0-0-2", "O-3-0-2-1", "X-1-1-2-0"],
        ["X-1-1-2-0", "O-3-1-2-0", "X-3-1-0-2", "O-3-1-1-0", "X-1-0-1-1"],
        ["X-2-1-2-0", "O-3-0-2-0", "X-1-1-0-0", "O-3-0-2-2", "X-1-0-1-0"],
        ["X-1-1-1-1", "O-2-0-1-1", "X-3-0-0-1", "O-2-0-2-2", "X-1-0-2-1"],
        ["X-1-1-2-2", "O-2-1-2-2", "X-2-0-0-2", "O-2-1-2-1", "X-1-0-1-2"],
        ["X-1-0-2-2", "O-2-0-2-2", "X-2-0-0-2", "O-2-0-1-2", "X-3-0-1-2"],
        ["X-1-0-1-1", "O-2-0-1-1", "X-1-1-0-0", "O-2-0-2-0", "X-2-0-2-2"],
        ["X-2-0-1-1", "O-3-1-1-1", "X-3-0-2-0", "O-3-1-0-0", "X-1-0-0-2"],
    ]

    count = 0
    for game in bad_games:
        for _ in range(10):
            board = Board()
            board.replay(game)
            board.undo(2)
            agent = Agent(board)
            agent.play()
            agent.play()

            if board.game_over:
                count += 1
    assert count == 0


def test_defend_multiple():
    """When I defend I should look for opportunities to block multiple
    In this situation O can only block both by covering at 0, 0
    """
    board = Board()
    agent = Agent(board)
    board.play("X", 1, 0, (0, 0))
    board.play("O", 1, 0, (1, 0))
    board.play("X", 1, 1, (0, 1))
    board.play("O", 1, 1, (1, 1))
    board.play("X", 2, 1, (1, 0))

    # Defend as O
    assert agent.defend()

    # X should not be able to win on the next move
    assert agent.check_winning_move() == False


def test_game_duration_with_defense():
    """When I play defense, games should take longer than not playing defense"""
    winning_moves = []
    for i in range(10):
        board = Board()
        agent = Agent(board)
        for _ in range(50):
            won = agent.check_winning_move()
            if not won:
                agent.random_play()
            if board.game_over:
                break
        winning_moves.append(len(board.moves))

    defending_moves = []
    for i in range(10):
        board = Board()
        agent = Agent(board)
        agent.play_out()
        defending_moves.append(len(board.moves))

    assert sum(defending_moves) > sum(winning_moves)
