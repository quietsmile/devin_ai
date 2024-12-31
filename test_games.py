"""
Test suite for verifying the implementation of the games.
"""
import twentyfour
import gomoku
import snake
import time

def test_twentyfour_game():
    print("\n=== Testing 24 Points Game ===")
    game = twentyfour.TwentyFourGame()
    print('Game initialized with numbers:', game.numbers)

    # Test expressions using actual game numbers
    numbers = game.numbers
    print('\nTesting solution checker with game numbers:', numbers)
    
    # Create test expressions using actual game numbers
    test_expressions = [
        f'{numbers[0]} + {numbers[1]} + {numbers[2]} + {numbers[3]}',
        f'{numbers[0]} * {numbers[1]} + {numbers[2]} + {numbers[3]}',
        f'({numbers[0]} + {numbers[1]}) * ({numbers[2]} + {numbers[3]})'
    ]

    print('\nTesting solution checker:')
    for expr in test_expressions:
        success, msg = game.check_solution(expr)
        print(f'\nExpression: {expr}')
        print(f'Result: {msg}')
        if success:
            print('Expression evaluates to:', eval(expr))

    # Test invalid expressions
    print('\nTesting invalid expressions:')
    invalid_tests = [
        'abc',  # Invalid format
        '1 + 2',  # Too few numbers
        '1 + 2 + 3 + 4 + 5',  # Too many numbers
        '1 ^ 2 + 3 + 4'  # Invalid operator
    ]

    for expr in invalid_tests:
        success, msg = game.check_solution(expr)
        print(f'\nExpression: {expr}')
        print(f'Result: {msg}')

    # Test solution existence
    print('\nTesting solution existence for different number sets:')
    test_numbers = [
        [1, 2, 3, 4],
        [2, 3, 7, 8],
        [4, 4, 8, 8]
    ]

    for nums in test_numbers:
        has_solution = game._has_solution(nums)
        print(f'Numbers {nums}: {"Has solution" if has_solution else "No solution"}')

def test_gomoku_game():
    print("\n=== Testing Gomoku Game ===")
    game = gomoku.GomokuGame()
    
    # Test board initialization
    print("\nTesting board initialization:")
    game.print_board()
    
    # Test making valid moves
    print("\nTesting valid moves:")
    moves = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]  # Should win for X
    for row, col in moves:
        success, msg = game.make_move(row, col)
        print(f"Move at ({row}, {col}): {msg}")
        game.print_board()
        if game.game_over:
            print("Game over:", msg)
            break

    # Test invalid moves
    print("\nTesting invalid moves:")
    game = gomoku.GomokuGame()
    invalid_moves = [
        (-1, 0),  # Out of bounds
        (15, 15), # Out of bounds
        (7, 7),   # Make valid move
        (7, 7)    # Try same position again
    ]
    
    for row, col in invalid_moves:
        success, msg = game.make_move(row, col)
        print(f"Move at ({row}, {col}): {msg}")

def test_snake_game():
    print("\n=== Testing Snake Game ===")
    game = snake.SnakeGame(width=10, height=10)  # Smaller board for testing
    
    # Test initial state
    print("\nInitial state:")
    game.print_board()
    print(f"Initial score: {game.score}")
    
    # Test movement and growth
    print("\nTesting movement and growth:")
    directions = [
        snake.Direction.RIGHT,
        snake.Direction.RIGHT,
        snake.Direction.DOWN,
        snake.Direction.LEFT
    ]
    
    for direction in directions:
        game.change_direction(direction)
        game.move()
        game.print_board()
        print(f"Score: {game.score}")
        time.sleep(0.5)  # Brief pause to see the movement
    
    # Test wall collision
    print("\nTesting wall collision:")
    game = snake.SnakeGame(width=5, height=5)
    # Move snake to left wall
    game.change_direction(snake.Direction.LEFT)
    success = game.move()
    print(f"Move into left wall - Game over: {game.game_over}")
    
    # Test right wall collision
    game = snake.SnakeGame(width=5, height=5)
    for _ in range(5):  # Move to right wall
        game.change_direction(snake.Direction.RIGHT)
        game.move()
    print(f"Move into right wall - Game over: {game.game_over}")
    
    # Test self collision
    print("\nTesting self collision:")
    game = snake.SnakeGame(width=5, height=5)
    
    # Set up a specific snake configuration for testing
    game.snake = [(2, 2), (2, 1)]  # Snake facing right
    game.direction = snake.Direction.RIGHT
    print("\nInitial snake position:")
    game.print_board()
    
    # Create a situation where snake will collide with itself
    print("\nCreating self collision scenario:")
    
    # Move right and eat food to grow
    game.food = (2, 3)  # Place food in path
    game.move()  # Move to (2, 3) and eat food
    print("\nAfter eating first food:")
    game.print_board()
    
    # Place another food and grow again
    game.food = (2, 4)
    game.move()  # Move to (2, 4) and eat food
    print("\nAfter eating second food:")
    game.print_board()
    
    # Move down
    game.change_direction(snake.Direction.DOWN)
    game.move()  # Move to (3, 4)
    print("\nAfter moving down:")
    game.print_board()
    
    # Move left
    game.change_direction(snake.Direction.LEFT)
    game.move()  # Move to (3, 3)
    print("\nAfter moving left:")
    game.print_board()
    
    # Move up - should collide with body
    game.change_direction(snake.Direction.UP)
    game.move()  # Should collide with body at (2, 3)
    print("\nAfter attempting to move up (should collide):")
    game.print_board()
    print(f"Self collision test - Game over: {game.game_over} (Expected: True)")
    print(f"Snake position: {game.snake}")  # Print snake segments for debugging

if __name__ == "__main__":
    print("Starting game tests...")
    test_twentyfour_game()
    test_gomoku_game()
    test_snake_game()
    print("\nAll tests completed!")
