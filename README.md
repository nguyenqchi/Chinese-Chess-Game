# Xiangqi AI bots with Minimax and CMA-ES Optimization

This is a multiplayer Chinese Chess game application for desktop that I built using Python3 and Pygame.

## Features

- Multiplayer support
- Intelligent agent using CMA-ES and Minimax algorithms
- Simulations for testing and training the agent

## Project Structure

- `game.py`: Contains the main game logic and the intelligent agent implementation.
- `mp_simulation.py`: Runs simulations to test and train the agent.
- `board.py`: Manages the game board and pieces.
- `pieces.py`: Defines the different types of pieces in the game.
- `utils.py`: Contains utility functions and constants.

## Intelligent Agent

The intelligent agent is built in the `game.py` file. It uses the Covariance Matrix Adaptation Evolution Strategy (CMA-ES) to optimize the weights for the Minimax algorithm, improving the decision-making process in the game.

## Simulations

Simulations are run in the `mp_simulation.py` file. These simulations are used to test and train the intelligent agent, ensuring it performs well in various scenarios.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nguyenqchi/chinese-chess-game.git
    cd chinese-chess-game
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the game:
    ```sh
    python game.py
    ```

2. Run simulations:
    ```sh
    python mp_simulation.py
    ```

## Attributes

The GUI of this project is cloned from Ngo Hong Quoc Bao's Chinese Chess repo
