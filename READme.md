# Enhanced Pong-style Table Tennis Game

This is an enhanced version of the classic Pong game, implemented in Python using the Pygame library. It features improved graphics, realistic physics, and exciting visual effects for a more engaging gameplay experience.

## Installation

1. Ensure you have Python 3.7+ installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/MonkWarrior08/Enhanced_Pong-1972.git
   cd Enhanced_Pong-1972
   ```

3. Install the required dependencies::
   ```
   pip install numpy pygame
   ```

4. Run the game:
   ```
   python pong.py
   ```

## How to Play

- Player 1 (Dimi): Use 'W' and 'S' keys to move the paddle up and down.
- Player 2 (Alice): Use 'Up' and 'Down' arrow keys to move the paddle up and down.
- Press 'Space' to start the game or restart after a game over.
- First player to score 5 points wins!

## Unique Features

This enhanced version of Pong includes several features that set it apart from the original game:

1. **Realistic Ball Physics**: 
   - The ball's movement includes acceleration and spin effects.
   - Spin is applied based on the paddle's movement direction when hit.

2. **Visual Enhancements**:
   - Colorful, rainbow-like trail effect for the ball.
   - Paddle movement leaves a fading trail.
   - Paddles have colorful auras (cyan for Dimi, magenta for Alice).
   - Dashed center line for improved visual appeal.

3. **Dynamic Backgrounds**:
   - Animated star field background for a space-like atmosphere.

4. **Improved Gameplay**:
   - Ball speed increases slightly with each hit, adding challenge.

5. **Sound Effects**:
   - Different sounds for ball hits and scoring.

6. **Winner Celebration**:
   - Colorful fireworks display when a player wins.

7. **Paddle Effects**:
   - Losing paddle shakes and turns red when a point is scored against it.

8. **Responsive Controls**:
   - Smooth paddle movement with trailing effect.

## License

This project is open source and available under the [MIT License](LICENSE).
