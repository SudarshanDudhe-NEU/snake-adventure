# Python Snake Game

A modern implementation of the classic Snake game using Python and Pygame with enhanced visual features and gameplay elements.

![Game Screenshot](assets/images/screenshot.png)

## Features

- Classic snake gameplay with modern graphics and animations
- Visually appealing snake with rounded head, eyes, flickering tongue, and tapered tail
- Realistic snake body with smooth transitions and scales
- Variety of food items (mice, eggs, frogs, birds, fruits, bugs) for the snake to eat
- Color-changing snake that adopts the color of consumed food
- Challenging obstacles to navigate around
- Pause/play functionality
- Score tracking
- Game over and restart functionality
- Configurable game speed and grid size

## Requirements

- Python 3.6+
- Pygame 2.5.2

## Installation

1. Clone this repository:

```
git clone https://github.com/SudarshanDudhe-NEU/snake-adventure.git
cd snake-adventure
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## How to Play

Run the game:

```
python src/main.py
```

### Controls:

- Arrow keys: Move the snake
- P: Pause/Resume the game
- Esc: Quit the game
- Enter: Restart after game over

## Game Rules

- Guide the snake to eat various food items (mice, eggs, frogs, etc.)
- Each food item increases your score by 10 points and makes your snake grow longer
- The snake changes color to match the food it just ate
- The game ends if the snake collides with itself or with obstacles
- The snake can pass through walls and appear on the opposite side

## Project Structure

```
snake-adventure/
├── src/
│   ├── main.py         # Game entry point
│   ├── game.py         # Game class with main game logic
│   ├── snake.py        # Snake class with visual enhancements
│   ├── food.py         # Food class with different food types
│   ├── obstacle.py     # Obstacle class
│   └── constants.py    # Game constants and settings
├── assets/
│   └── sounds/         # Game sound effects (if added)
├── requirements.txt    # Python dependencies
├── LICENSE            # MIT License file
└── README.md           # This file
```

## Visual Enhancements

- **Snake**: Features a rounded head with eyes, flickering tongue, scaled body segments with smooth transitions at corners, and a tapered tail
- **Food**: Various visually distinct food types that snakes typically eat
- **Color System**: Dynamic color-changing snake based on consumed food
- **Obstacles**: Challenging obstacles that require strategic navigation

## Development

Feel free to fork this project and make your own modifications. Some ideas for enhancements:

- Add sound effects for eating, game over, etc.
- Implement special food items with power-ups (speed boost, invincibility, etc.)
- Create progressive difficulty levels with more obstacles or faster gameplay
- Add a high score system with local or online leaderboards
- Implement different snake skins or themes

## License

This project is licensed under the MIT License - see the LICENSE file for details.
