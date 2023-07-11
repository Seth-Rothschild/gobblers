# About
This is an implementation of gobblers, for the purpose of storing games and recreating games from records.

# Notation
A piece has a `player` (X or Y), a `size` (1, 2, or 3) and an `index` (0 or 1). While the first two are self explanatory, the index is used to differentiate between the first and second copy of a piece that belongs to a player.

As an example, we might notate a move `X-2-0-1-1` to mean
  1. The player is `X`
  2. The size is 2, the middle size
  3. This is the first of the two middle sized `X` pieces as indicated by the 0
  4. The move is played at `(1, 1)`, the center of the board.

This notation is annoying to write by hand, but programatically convenient.


# Install
First install [miniforge](https://github.com/conda-forge/miniforge) and then run `make install`. To check that it's working, run `make test`.

