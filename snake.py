"""
Snake Game Implementation
A classic game where the player controls a snake that grows longer as it eats food,
while avoiding collisions with walls and itself.
"""

import random
import time
import os
import sys
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.snake = [(height//2, width//2)]  # Start at center
        self.direction = Direction.RIGHT
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False
        self.growing = False  # Track if snake is currently growing

    def _spawn_food(self):
        """Spawn food at a random empty position."""
        while True:
            food = (random.randint(0, self.height-1), 
                   random.randint(0, self.width-1))
            if food not in self.snake:
                return food

    def move(self):
        """Move the snake one step in the current direction."""
        if self.game_over:
            return False

        # Calculate new head position
        head = self.snake[0]
        if self.direction == Direction.UP:
            new_head = (head[0]-1, head[1])
        elif self.direction == Direction.DOWN: 
            new_head = (head[0]+1, head[1])
        elif self.direction == Direction.LEFT:
            new_head = (head[0], head[1]-1)
        else:  # Direction.RIGHT
            new_head = (head[0], head[1]+1)

        # Check for collisions with walls
        if (new_head[0] < 0 or new_head[0] >= self.height or
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return False

        # Check for collisions with self
        # When growing, check against entire snake
        # When not growing, exclude the tail since it will be removed
        snake_body = self.snake[:-1] if not self.growing else self.snake
        if new_head in snake_body:
            self.game_over = True
            return False

        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
            self.growing = True
        else:
            self.growing = False
            self.snake.pop()
        
        return True

    def change_direction(self, new_direction):
        """Change the snake's direction if valid."""
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if opposite_directions[new_direction] != self.direction:
            self.direction = new_direction

    def get_board(self):
        """Return the current game board as a 2D array."""
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place food
        board[self.food[0]][self.food[1]] = '*'
        
        # Place snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                board[segment[0]][segment[1]] = '@'  # Head
            else:
                board[segment[0]][segment[1]] = 'O'  # Body
                
        return board

    def print_board(self):
        """Print the current game board."""
        board = self.get_board()
        
        # Clear screen (works on both Windows and Unix-like systems)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print top border
        print(' ' + '-' * (self.width * 2 + 1))
        
        # Print board with side borders
        for row in board:
            print('|' + ' '.join(row) + '|')
        
        # Print bottom border
        print(' ' + '-' * (self.width * 2 + 1))
        print(f'Score: {self.score}')

def main():
    """Main game loop."""
    game = SnakeGame()
    print("Welcome to Snake!")
    print("Use WASD keys to move:")
    print("W - Up")
    print("S - Down")
    print("A - Left")
    print("D - Right")
    print("Press Enter to start...")
    input()

    while not game.game_over:
        game.print_board()
        
        # Non-blocking input (simplified version)
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            key = sys.stdin.read(1).lower()
            if key == 'w':
                game.change_direction(Direction.UP)
            elif key == 's':
                game.change_direction(Direction.DOWN)
            elif key == 'a':
                game.change_direction(Direction.LEFT)
            elif key == 'd':
                game.change_direction(Direction.RIGHT)
        
        game.move()
        time.sleep(0.2)  # Control game speed

    print("\nGame Over!")
    print(f"Final Score: {game.score}")

if __name__ == "__main__":
    try:
        import select
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
