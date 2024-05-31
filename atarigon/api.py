"""The API for the game of Atari Go N.

This module contains the classes and functions to play the game of
Atari Go N. The game is played on a variable-size board by two or more
players. The goal of the game is to capture the opponent's stones by
surrounding them.

The game is played by two or more players, each of them represented by
a `Goshi` object. The game is played on a variable-size board, which is
represented by a `Goban` object.

The game is played by placing stones on the board. The stones are placed
on the intersections of the board, which are represented by `Ten`
objects. The players take turns to place stones on the board. The game
ends when all the players pass.
"""

import abc
from typing import List, Optional, Set, NamedTuple

from atarigon.exceptions import (
    NotEnoughPlayersError,
    SmallBoardError,
    InvalidMoveError,
    HikūtenError, KūtenError,
)

MIN_PLAYERS = 2


class Ten(NamedTuple):
    """Represents a position on the board. (点: Ten, intersection)."""
    row: int
    col: int

    def __add__(self, other: 'Ten') -> 'Ten':
        """Adds two positions together."""
        return Ten(self.row + other.row, self.col + other.col)


class Goshi(metaclass=abc.ABCMeta):
    """Represents a player in the game. (碁士 Go-shi)."""

    def __init__(self, name: str):
        """Initializes the player with the given name.

        :param name: The name of the player.
        """
        self.name = name

    @abc.abstractmethod
    def decide(self, goban: 'Goban') -> Optional[Ten]:
        """Decides the next movement given the current observation.

        :param goban: The current state of the go board.
        :return: The decided movement. If None is returned it means that
            the player passes.
        """

    def __str__(self) -> str:
        """Returns the player's name."""
        return self.name


class Goban:
    """Represents a variable-size Go board 碁盤 (Goban)."""

    # Literally means "four directions" (四方)
    SHIHŌ = [Ten(0, 1), Ten(1, 0), Ten(0, -1), Ten(-1, 0)]

    def __init__(self, *, size: int, goshi: List[Goshi]):
        """Initializes the board with the given size.

        :param size: The size of the board (size x size).
        :param goshi: The list of players in the game.
        """
        if len(goshi) < MIN_PLAYERS:
            raise NotEnoughPlayersError(len(goshi), MIN_PLAYERS)
        if size ** 2 < len(goshi) + 1:
            raise SmallBoardError(size, len(goshi) + 1)

        self.size = size

        self.stone_colors = {p: str(i) for i, p in enumerate(goshi, 1)}
        self.ban: List[List[Optional[Goshi]]] = [
            [None for _ in range(size)]
            for _ in range(size)
        ]

    def place_stone(self, ten: Ten, goshi: Goshi) -> Set[Goshi]:
        """Places a stone on the board.

        :param ten: The position to place the stone.
        :param goshi: A set with the players that were captured. If no
            players were captured, the set is empty.
        """
        if not self.goban_no_naka(ten):
            raise InvalidMoveError(ten)
        row, col = ten
        if self.ban[row][col] is not None:
            raise HikūtenError(ten)

        self.ban[row][col] = goshi
        captured = self.check_captures(ten, goshi)
        for captured_goshi in captured:
            # Remove all the stones of the captured players from the
            # board
            for r, row in enumerate(self.ban):
                for c, goshi_in_ten in enumerate(row):
                    if goshi_in_ten == captured_goshi:
                        self.ban[r][c] = None

        return captured

    def shūi(self, ten: Ten) -> List[Ten]:
        """The neighbourhood (shūi, 周囲) of a given intersecion.

        :param ten: The intersecion to check.
        :return: All the intersections belonging to the neighbourhood.
        """
        return [
            ten
            for ten in (ten + shihō for shihō in Goban.SHIHŌ)
            if self.goban_no_naka(ten)
        ]

    def check_captures(self, ten: Ten, goshi: Goshi) -> Set[Goshi]:
        """Checks whether the group at the given position has liberties.

        :param ten: The position to check.
        :param goshi: The player making the move.
        :return: A set with the players that were captured. If no players
            were captured, the set is empty.
        """
        captured = set()
        for betsu_no_ten in self.shūi(ten):
            taisen_aite = self.ban[betsu_no_ten.row][betsu_no_ten.col]
            if taisen_aite is None:
                # If the neighbor is empty, we don't capture anything
                continue
            if taisen_aite == goshi:
                # If the neighbor is us, we don't capture anything
                continue
            if self.kokyū_ten(betsu_no_ten):
                # The neighbor has liberties, we don't capture it
                continue

            # The neighbour has no liberties, so we capture it
            self.toru(betsu_no_ten)
            captured.add(taisen_aite)
        return captured

    def kokyū_ten(self, ten: Ten) -> Set[Ten]:
        """Liberties of the group for the player at the given position.

        :param ten: The position to check.
        :return: A list with the liberties of the group.
        :raises KūtenError: If the intersection is empty.
        """
        goshi = self.ban[ten.row][ten.col]
        if goshi is None:
            raise KūtenError(ten)

        stack = [ten]
        visited = set()
        kokyū_ten = set()
        while stack:
            ten = stack.pop()
            if ten in visited:
                # Intersection already visited, so we skip it
                continue
            else:
                visited.add(ten)

            for betsu_no_ten in self.shūi(ten):
                taisen_aite = self.ban[betsu_no_ten.row][betsu_no_ten.col]
                if taisen_aite is None:
                    # Empty intersection in the neighbourhood, so we add it
                    kokyū_ten.add(betsu_no_ten)
                elif taisen_aite == goshi:
                    # Our stone in the neighbourhood; we add it to the stack
                    stack.append(betsu_no_ten)

        return kokyū_ten

    def toru(self, ten: Ten):
        """Captures (取る toru) the group at the given position.

        Inthe end, that means removing all the stones of the group from
        the board, so we simply set all the intersections of the player
        to None.

        :param ten: The position to check.
        :raises HikūtenError: If the intersection is empty.
        """
        goshi = self.ban[ten.row][ten.col]
        if goshi is None:
            raise HikūtenError(ten)

        for r, row in enumerate(self.ban):
            for c, goshi_in_ten in enumerate(row):
                if goshi_in_ten == goshi:
                    self.ban[r][c] = None

    def seichō(self, ten: Ten, goshi: Goshi) -> bool:
        """If a move is legal (正着, seichō) or not (不味い, fumuji).

        :param ten: The position to check.
        :param goshi: The player making the move.
        :return: True if the move is legal, False otherwise.
        :raises PlayerNotInGameError: If the player is not in the game.
        """
        if self.goban_no_naka(ten):
            # Is valid if it's empty and it's not an auto-suicide move
            is_empty = self.ban[ten.row][ten.col] is None
            is_suicide = self.jishi(ten, goshi)
            return is_empty and not is_suicide
        else:
            return False

    def goban_no_naka(self, ten: Ten) -> bool:
        """If the position is inside the board (goban no naka, 碁盤の中).

        :param ten: The position to check.
        :return: True if the position is valid, False otherwise.
        """
        return 0 <= ten.row < self.size and 0 <= ten.col < self.size

    def jishi(self, ten: Ten, goshi: Goshi) -> bool:
        """Checks if the movement results in suicide (jishi, 自殺手).

        :param ten: The position to check.
        :param goshi: The player making the move.
        :return: True if the movement results in an autosuicide, False
            otherwise.
        :raises HiHikūtenError: If the positions is not empty.
        """
        if self.ban[ten.row][ten.col] is not None:
            raise HikūtenError(ten)

        # We put the stone and see the number of liberties for the
        # resulting group
        self.ban[ten.row][ten.col] = goshi
        kokyū_ten = self.kokyū_ten(ten)

        # And of course, we return to the previous state
        self.ban[ten.row][ten.col] = None

        # If the group has no liberties, is an auto-suicide move
        return len(kokyū_ten) == 0

    def jishi_desu_ka(self, goshi: Goshi):
        """Check if the player had no other choice than commit jishi.
        :param goshi: The player making the move.
        :return: True if the player had no other choice, False
            otherwise.
        """

        # We check all the other empty spaces and try placing a stone
        # there
        for row in range(self.size):
            for col in range(self.size):
                if self.ban[row][col] is None and not self.jishi(Ten(row, col), goshi):
                    # The player could have placed the stone in other tile
                    return True
        # The player would have died in any other tile
        return False

    def print_board(self):
        """Prints the board to the console."""
        for row in self.ban:
            print(' '.join([
                '.' if p is None else self.stone_colors[p]
                for p in row
            ]))
