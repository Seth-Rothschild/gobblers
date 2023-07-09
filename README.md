# About
This is an implementation of gobblers, for the purpose of storing games and recreating games from records.

# Notation
A piece has a `player` (X or Y), a `size` (1, 2, or 3) and an `index` (0 or 1). While the first two are self explanatory, the index is used to differentiate between the first and second copy of a piece that belongs to a player.

As an example if we write `XX0-1-1` we mean that the middle sized X piece is being placed in the center. That means that `OOO-1-1` is still a valid move. If X plays `XX1-0-0` that is referencing their _second_ middle sized piece.

# Install
First install [miniforge](https://github.com/conda-forge/miniforge) and then run `make install`. To check that it's working, run `make test`.

