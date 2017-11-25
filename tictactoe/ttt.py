import random
from enum import Enum


class Player(Enum):
    """
    Players as enumerated constants
    """
    FIRST = 'O'
    SECOND = 'X'
    THIRD = '-'


def game_intro():
    """
    Show the introduction text
    """
    print("\n\n\t\t\t---------------------------------------------")
    print("\t\t\t    ~Welcome to 3 player Tic Tac Toe Game~   ")
    print("\t\t\t---------------------------------------------")
    print("\t\t\t      Each Player has a different symbol     ")
    print("\t\t\t             (X) or (-) or (O)               ")
    print("\t\t\t  Place your symbol in any line of 3 to win\n")


def game_init(grid_values, grid_size, current_player):
    """
    Init the game
    Params:
        grid_values: list
            The grid's value
        grid_size: int
            The grid size
        current_player: Player
            The current player
    Return:
        None
    """
    # Show the grid
    show_game(grid_values, grid_size)
    print("\n\t\t\t '{}' has been chosen to go first".format(current_player.value))


def show_game(grid_values, grid_size):
    """
    Show the grid to console
    Params:
        grid_values: list
            The grid's value
        grid_size: int
            The grid size
    Return:
        None
    """
    print("\n")
    # Just for formating
    print('     ', end='')
    for i in range(grid_size):
        # Print the top row indicate the column index
        print('  ' + str(i + 1) + '   ', end='')
    for i in range(grid_size):
        print()
        # '------' * grid_size means we multiple the string '------' grid_size times
        # Example: 'a' * 3 will be '***'
        # This line prints the horizontal line with width depends on the size of the grid
        # -----------------------------------------
        print('    ' + '------' * grid_size + '-')

        # When if i > 8, (i + 1) will be >= 10 which has 2 characters
        # We have to remove 1 space after the row index
        # By this way, the printed grid won't be 'crashed'
        print(' ' + str(i + 1) + (' |' if i > 8 else '  |'), end='')

        # Print the grid value i.e the empty string or symbols(O, X, -)
        for j in range(grid_size):
            print('  ' + str(grid_values[i][j]) + '  |', end='')

    print()
    # Print the bottom line
    print('    ' + '------' * grid_size + '-')


def chose_first_player():
    """
    Randomly chose the player who will make first step
    """
    # Make enum iterable using list(EmumClass)
    # index = random.randrange(len(list(Player)))
    # return list(Player)[index]
    return Player.SECOND


def next_player(current_player):
    """
    Chose next player base on current player
    Params:
        current_player: Player
            The current player
    Return:
        next_player: Player
            The next player who will play next step
    """
    # It's just a circle turn
    if current_player == Player.FIRST:
        return Player.SECOND
    elif current_player == Player.SECOND:
        return Player.THIRD
    return Player.FIRST


def play(current_player, grid_values, grid_size):
    """
    Game playing
    Params:
        grid_values: list
            The grid's value
        grid_size: int
            The grid size
        current_player: Player
            The current player
    Return:
        None
    """
    # Number of free cells in grid
    free_squares = grid_size * grid_size
    while True:
        # To access the value of enum instance, use value property
        # Ex: current_player.value
        # This will be 'O', 'X' or '-' depend on who is current player
        print("\n\t\t\tYour turn: '{}'".format(current_player.value))
        while True:
            try:
                row = input("Select row to place    : " +
                            current_player.value + " : ")
                slot_x = (int)(row) - 1
                col = input("Select column to place : " +
                            current_player.value + " : ")
                slot_y = (int)(col) - 1
                # Check if user input the row/column index in valid range
                if slot_x in range(0, grid_size) and slot_y in range(0, grid_size):
                    # If chosen cell is free
                    if slot_free(grid_values, slot_x, slot_y):
                        # Then put the symbol to it
                        grid_values[slot_x][slot_y] = current_player.value
                        break
                    else:
                        print("\n**Someone already took that slot**\n")
                else:
                    print(
                        '\n** Please only enter between (1 - {}) as indicated on grid **\n'.format(grid_size))

            except ValueError:
                # When user input value which can not cast to integer
                print("\n**ERROR** Please enter INTEGER!!**\n")

        # After every turn, we update the grid and show the updated grid to screen
        show_game(grid_values, grid_size)

        # Check to see if any player wins
        check_for_winner(grid_values, grid_size)

        # After every turn, 1 cell will be filled then the free cells will be descreased
        free_squares -= 1
        # Stop game when entire grid is filled
        if free_squares == 0:
            print("\n**Game Over** No Winners and No space left\n")
            break
        
        # or when there is a winner
        if check_for_winner(grid_values, grid_size):
            print("\n\t\t\t**Winner Winner Winner**!!\n")
            print("\n\t\t\tCongratulation '" +
                  current_player.value + "' WON!!!")
            break
        # this is for changing players turn by turn
        current_player = next_player(current_player)


def check_straight(grid_values, grid_size):
    """
    Check if there are 3 adjacent same 'symbol' s on same row/column
    Params:
        grid_values: list
            The grid's value
        grid_size: int
            The grid size
        current_player: Player
            The current player
    Return:
        True: If there are 3 adjacent same 'symbol' s on same row/column
        None: Otherwise
    """
    # 'O', 'X', '-
    symbols = [p.value for p in Player]
    for x in range(0, grid_size):
        for n in range(0, grid_size - 2):
            for symbol in symbols:
                # Check if 3 same 'symbol's  are adjacent in one column
                vertical_matching = grid_values[x][n] \
                    == grid_values[x][n + 1] \
                    == grid_values[x][n + 2] == symbol

                if vertical_matching:
                    return True

                # Check if 3 same 'symbol's  are adjacent in one row
                horizontal_matching = grid_values[n][x] \
                    == grid_values[n + 1][x] \
                    == grid_values[n + 2][x] == symbol

                if horizontal_matching:
                    return True


def check_diagonal_line(grid_values, grid_size):
    """
    Check if there are 3 adjacent same 'symbol' s on  same diagonal line
    Params:
        grid_values: list
            The grid's value
        grid_size: int
            The grid size
    Return:
        True: If there are 3 adjacent same 'symbol' s on same diagonal line
        None: Otherwise
    """
    # 'O', 'X', '-
    symbols = [p.value for p in Player]
    # Check on \\\ diagonals
    # |__|__
    #    |__|__
    #       |__|
    for x in range(0, grid_size - 2):
        for y in range(0, grid_size - 2):
            for symbol in symbols:
                if grid_values[y][x] == grid_values[y + 1][x + 1] == grid_values[y + 2][x + 2] == symbol:
                    return True
    
    # Check on /// diagonals
    #      __|__|
    #  ___|__|
    # |__|
    for x in range(2, grid_size):
        for y in range(0, grid_size - 2):
            for symbol in symbols:
                if grid_values[x][y] == grid_values[x - 1][y + 1] == grid_values[x - 2][y + 2] == symbol:
                    return True


def check_for_winner(grid_values, grid_size):
    if check_straight(grid_values, grid_size) or check_diagonal_line(grid_values, grid_size):
        return True


def slot_free(grid_values, x, y):
    # If the cell is not in ['O', 'X', '-'], it is free
    return True if grid_values[x][y] == ' ' else False


def get_grid_size_from_user():
    while True:
        try:
            grid_size = input('Please enter the grid size (5 - 10): ')
            grid_size = int(grid_size)
            if 5 <= grid_size <= 10:
                return grid_size
        except ValueError:
            print("\n**ERROR** Please enter INTEGER!!**\n")


def main():
    game_intro()
    grid_size = get_grid_size_from_user()
    # Initialize grid values are ' '
    # Grid is a square with size grid_size x grid_size
    grid_values = [[' ' for i in range(grid_size)] for i in range(grid_size)]
    current_player = chose_first_player()
    game_init(grid_values, grid_size, current_player)
    play(current_player, grid_values, grid_size)


if __name__ == '__main__':
    main()
