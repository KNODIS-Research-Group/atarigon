import random
from typing import Optional

from atarigon.api import Goshi, Goban, Ten


class NinjaGoshi(Goshi):
    """Player that makes random moves.

    You'll never know what it's going to do next!
    """

    def __init__(self):
        """Initializes the player with the given name."""
        super().__init__(f'Ninja')

    def decide(self, goban: 'Goban') -> Optional[Ten]:
        """Gets a random empty position in the board.

        :param goban: The current observation of the game.
        :return: The next move as a (row, col) tuple.
        """
        # Finds all the empty positions in the observation
        empty_positions = [
            Ten(row, col)
            for row in range(len(goban.ban))
            for col in range(len(goban.ban[row]))
            if goban.ban[row][col] is None
        ]

        # Chooses a random valid empty position
        random.shuffle(empty_positions)
        for ten in empty_positions:
            if goban.ban[ten.row][ten.col] is None:
                return ten
        else:
            return None
