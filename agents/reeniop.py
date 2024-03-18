from typing import Optional

from atarigon.api import Goshi, Goban, Ten


class Reeniop(Goshi):
    """Like pioneer, but backwards."""

    def __init__(self):
        """Initializes the player."""
        super().__init__(f'Reeniop')

    def decide(self, goban: 'Goban') -> Optional[Ten]:
        """Gets the last empty position in the board.

        :param goban: The current observation of the game.
        :return: The next move as a (row, col) tuple.
        """
        for row in range(goban.size - 1, -1, -1):
            for col in range(goban.size - 1, -1, -1):
                if goban.ban[row][col] is None:
                    return Ten(row, col)
        return None
