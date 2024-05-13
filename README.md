# AtariGoN

AtariGoN is a simulation environment based on the Atari Go rules, for
two or more players. The game is played on a board with size NxN, and
the players take turns placing their stones on the intersections of the
board. The goal of the game is being the last player to place a stone on
the board. The game ends when no player can place a stone on the board
without being captured or when only one player can place a stone on the
board.

The project aims to provide a versatile environment for testing
different AI algorithms and strategies, and to provide a platform for
research and educational purposes.

## Features

- **Multi-Agent support**: Allows for games between multiple,
  user-defined automated agents, fostering a competitive or
  collaborative AI research environment.
- **Customizable board sizes**: Accommodates various styles of play by
  allowing users to specify the board size, supporting standard sizes (
  9x9, 13x13, and 19x19), but not limited to them.
- **Multiple game simulation**: Facilitates the simulation of multiple
  games in succession, generating a comprehensive leaderboard to track
  agent performance over time.
- **Dynamic Agent Integration**: Leverages dynamic module loading,
  enabling users to add or update agents without altering the core
  simulation code.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python 3.8 or later installed on your
system. This version or newer is required due to the use of recent
enhancements in the Python typing module and other features.

### Installation

1. Clone the repository to your local machine using the following
   command:
    ```bash
    git clone https://github.com/KNODIS-Research-Group/atarigon.git
    cd atarigon
   ```
2. Install the project dependencies using Poetry:
    ```bash
    poetry install
    ```
3. No external dependencies are required outside the standard
   Python library, making it straightforward to set up and run.

It should be noted that the project uses the Poetry package manager for
dependency management and packaging. If you don't have Poetry installed
on your system, you can install it by following the instructions on the
[official website](https://python-poetry.org/docs/).

### Running the simulation

Execute the simulator with the command below, replacing the
angle-bracketed parameters with your desired settings:

```bash
poetry run python atarigon/main.py --size <board_size> \\
               --agents <path_to_agents_directory> \\
               --games <number_of_games>
```

For example, to run a simulation with a 9x9 board, using the agents
located in the `agents` directory, and simulating 1000 games, you would
run the following command:

```bash
poetry run python atarigon/main.py --size 9 --agents agents --games 1000
```

Parameters:

- `--size`: The size of the Go board (9, 13, or 19 are standard sizes).
- `--agents`: The directory containing the Python files for your Go
  agents.
- `--games`: The number of games to simulate (default is 1).

### Custom agent development

To develop your own agent, create a Python class that extends the
`Goshi` class. Your class should implement the abstract methods defined
in Goshi, allowing it to decide on moves and interact with the game
board.

Place the `.py` file for your agent in the directory specified by the
`--agents` parameter when running the simulator. For examples and best
practices, refer to the agent templates provided in the repository.

## Contributing

Contributions are warmly welcomed. Whether you're fixing a bug, adding
a new feature, improving the documentation, ... whatever; your help is
deeply appreciated.

To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push the branch to your fork.
5. Submit a pull request against the main repository.

Please adhere to the code style guidelines and include unit tests for
new features or fixes. For more information, see the `CONTRIBUTING.md`
file in the repository.

## License

This project is licensed under the GNU General Public License v3.0.
For more information, see the LICENSE file in the repository.