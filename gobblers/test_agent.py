from gobblers.agent import Agent
from gobblers.board import Board, Gobbler

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
