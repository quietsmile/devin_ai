"""
24 Points Game Implementation
A mathematical game where players try to make 24 using four numbers and basic operations.
"""

import random
import itertools
import operator

class TwentyFourGame:
    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        self.numbers = self._generate_numbers()

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
        Supports both simple format (num1 op num2 op num3 op num4)
        and expressions with parentheses.
        """
        try:
            # Extract all numbers from the expression
            import re
            nums_in_expr = [int(n) for n in re.findall(r'\d+', expression)]
            
            # Verify all numbers are used exactly once
            if sorted(nums_in_expr) != sorted(self.numbers):
                return False, "Numbers don't match the game numbers"

            # Verify only valid operators are used
            valid_chars = set('0123456789+-*/() ')
            if not all(c in valid_chars for c in expression):
                return False, "Invalid characters in expression"

            # Evaluate the expression
            try:
                result = eval(expression)
                if abs(result - 24) < 0.0001:
                    return True, "Correct! The expression equals 24!"
                else:
                    return False, f"Expression equals {result}, not 24"
            except ZeroDivisionError:
                return False, "Division by zero is not allowed"
            except Exception as e:
                return False, "Invalid expression format"

        except Exception as e:
            return False, "Invalid expression format"

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
