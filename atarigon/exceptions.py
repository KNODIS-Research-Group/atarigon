"""Exceptions for the Aratigon game.

This module contains the exceptions that are raised by the game.
"""


class AtarigonError(Exception):
    """Base class for exceptions in this module."""
    pass


class NotEnoughPlayersError(AtarigonError):
    """Exception raised when there are not enough players."""

    def __init__(self, num_players: int, min_players: int):
        self.num_players = num_players
        super().__init__(f'At least {min_players} players required, but '
                         f'{num_players} were given')


class SmallBoardError(AtarigonError):
    """Exception raised when the board is too small."""

    def __init__(self, size: int, min_size: int):
        self.size = size
        super().__init__(f'Board size must be at least {min_size}, but '
                         f'{size} was given')


class InvalidMoveError(AtarigonError):
    """Exception raised for invalid moves."""

    def __init__(self, ten: 'Ten'):
        super().__init__(f'Invalid move: {ten}')


class PositionError(AtarigonError):
    """Exception raised when a position is invalid."""

    def __init__(self, ten: 'Ten', empty: bool):
        status = 'empty' if empty else 'not empty'
        super().__init__(f'{ten} is {status}')


class KūtenError(PositionError):
    """Empty intersection (Kūten 空点) when it should not be."""

    def __init__(self, ten: 'Ten'):
        super().__init__(ten, empty=True)


class HikūtenError(PositionError):
    """Not empty intersecion (非空点 Hikūten) when it should be."""

    def __init__(self, ten: 'Ten'):
        super().__init__(ten, empty=False)
