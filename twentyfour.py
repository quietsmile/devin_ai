"""
24 Points Game Implementation
A mathematical game where players try to make 24 using four numbers and basic operations.
"""

import random
import itertools
import operator

class TwentyFourGame:
    def __init__(self):
        self.numbers = self._generate_numbers()
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }

    def _generate_numbers(self):
        """Generate four random numbers that have at least one solution."""
        while True:
            numbers = [random.randint(1, 13) for _ in range(4)]
            if self._has_solution(numbers):
                return numbers

    def _evaluate(self, nums, ops):
        """Evaluate an expression with given numbers and operators."""
        try:
            # First operation
            result = ops[0](nums[0], nums[1])
            
            # Second operation
            if len(nums) > 2:
                result = ops[1](result, nums[2])
            
            # Third operation
            if len(nums) > 3:
                result = ops[2](result, nums[3])
            
            return result
        except ZeroDivisionError:
            return None

    def _has_solution(self, numbers):
        """Check if the given numbers have at least one solution."""
        for nums in itertools.permutations(numbers):
            for ops in itertools.product(self.operations.values(), repeat=3):
                result = self._evaluate(nums, ops)
                if result is not None and abs(result - 24) < 0.0001:
                    return True
        return False

    def check_solution(self, expression):
        """
        Check if the given expression equals 24.
        Expression should be in the format: "num1 op num2 op num3 op num4"
        """
        try:
            # Split expression into tokens
            tokens = expression.split()
            if len(tokens) != 7:  # 4 numbers and 3 operators
                return False, "Invalid expression format"

            # Convert numbers to float and validate they match the game numbers
            nums = [float(tokens[i]) for i in range(0, 7, 2)]
            ops = [tokens[i] for i in range(1, 7, 2)]
            
            # Check if used numbers match the game numbers
            game_nums_sorted = sorted(self.numbers)
            solution_nums_sorted = sorted([int(n) for n in nums])
            if game_nums_sorted != solution_nums_sorted:
                return False, "Numbers don't match the game numbers"

            # Validate operators
            if not all(op in self.operations for op in ops):
                return False, "Invalid operators"

            # Evaluate expression
            result = nums[0]
            for i in range(3):
                result = self.operations[ops[i]](result, nums[i + 1])

            # Check if result is 24
            if abs(result - 24) < 0.0001:
                return True, "Correct! The expression equals 24!"
            else:
                return False, f"Expression equals {result}, not 24"

        except (ValueError, ZeroDivisionError, KeyError) as e:
            return False, f"Invalid expression: {str(e)}"

def main():
    """Main game loop."""
    game = TwentyFourGame()
    print("Welcome to the 24 Points Game!")
    print("Make 24 using these four numbers and basic operations (+, -, *, /)")
    print("Enter your solution in the format: num1 op num2 op num3 op num4")
    print("Example: 3 + 4 * 5 - 1")
    print("\nYour numbers are:", ' '.join(map(str, game.numbers)))
    
    while True:
        try:
            expression = input("\nEnter your solution (or 'q' to quit): ")
            if expression.lower() == 'q':
                print("Thanks for playing!")
                break
                
            success, message = game.check_solution(expression)
            print(message)
            
            if success:
                play_again = input("\nPlay again? (y/n): ")
                if play_again.lower() != 'y':
                    print("Thanks for playing!")
                    break
                game = TwentyFourGame()
                print("\nNew numbers:", ' '.join(map(str, game.numbers)))
                
        except KeyboardInterrupt:
            print("\nGame terminated by user")
            break

if __name__ == "__main__":
    main()
