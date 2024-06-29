# Pong-style Table Tennis Game

This is a simple Pong-style table tennis game implemented in Python using the Pygame library. The game features two paddles controlled by different keys, a ball that bounces between them, and a scoring system. It also includes sound effects for ball collisions.

## Prerequisites

Before you can run the game, you need to have the following installed on your system:

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/your-username/pong-game.git
   cd pong-game
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install pygame numpy
   ```

## How to Play

1. Run the game:
   ```
   python pong_game.py
   ```

2. Controls:
   - Player 1 (Dimi, left paddle):
     - W: Move paddle up
     - S: Move paddle down
   - Player 2 (Alice, right paddle):
     - Up Arrow: Move paddle up
     - Down Arrow: Move paddle down
   - Spacebar: Start each round

3. Scoring:
   - Each time the ball passes a paddle, the opposite player scores a point.
   - The game ends when a player reaches 10 points.

## Features

- Two-player gameplay
- Sound effects for ball collisions
- Score display
- Winner announcement

## Customization

You can customize various aspects of the game by modifying the constants at the beginning of the `pong_game.py` file, such as:

- Screen dimensions
- Paddle and ball sizes
- Game speed
- Winning score

## Contributing

Feel free to fork this repository and submit pull requests with any improvements or bug fixes you'd like to contribute.

## License

This project is open source and available under the [MIT License](LICENSE).

