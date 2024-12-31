"""
Gomoku (Five in a Row) game implementation
A two-player board game where players alternate placing pieces on a board,
trying to get five in a row horizontally, vertically, or diagonally.
"""

class GomokuGame:
    def __init__(self, size=15):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def print_board(self):
        """Print the current state of the board."""
        # Print column numbers
        print('   ' + ' '.join(f'{i:2}' for i in range(self.size)))
        # Print rows
        for i in range(self.size):
            print(f'{i:2} |' + '|'.join(f'{cell:2}' for cell in self.board[i]) + '|')

    def make_move(self, row, col):
        """Attempt to make a move at the specified position."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, "Position out of bounds"
        if self.board[row][col] != ' ':
            return False, "Position already occupied"
        
        self.board[row][col] = self.current_player
        if self._check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True, f"Player {self.current_player} wins!"
        
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True, "Move successful"

    def _check_win(self, row, col):
        """Check if the last move at (row, col) resulted in a win."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal
        for dr, dc in directions:
            count = 1
            # Check in positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
                count += 1
                r, c = r + dr, c + dc
            # Check in negative direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
                count += 1
                r, c = r - dr, c - dc
            if count >= 5:
                return True
        return False

def main():
    """Main game loop."""
    game = GomokuGame()
    print("Welcome to Gomoku!")
    print("Players take turns placing X and O on the board.")
    print("First to get 5 in a row (horizontally, vertically, or diagonally) wins!")
    
    while not game.game_over:
        game.print_board()
        print(f"\nPlayer {game.current_player}'s turn")
        try:
            row = int(input("Enter row number: "))
            col = int(input("Enter column number: "))
            success, message = game.make_move(row, col)
            print(message)
        except ValueError:
            print("Please enter valid numbers")
    
    # Final board state
    game.print_board()
    if game.winner:
        print(f"\nCongratulations! Player {game.winner} wins!")

if __name__ == "__main__":
    main()
