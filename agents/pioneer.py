from typing import Optional

from atarigon.api import Goshi, Goban, Ten


class Pioneer(Goshi):
    """The player claims the first empty position it finds."""

    def __init__(self):
        """Initializes the player."""
        super().__init__(f'Pioneer')

    def decide(self, goban: 'Goban') -> Optional[Ten]:
        """Gets the first empty position in the board.

        :param goban: The current observation of the game.
        :return: The next move as a (row, col) tuple.
        """
        for row in range(len(goban.ban)):
            for col in range(len(goban.ban[row])):
                if goban.ban[row][col] is None:
                    return Ten(row, col)
        return None
