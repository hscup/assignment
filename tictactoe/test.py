from enum import Enum

class Color(Enum):
    FIRST   = 'O'
    SECOND  = 'X'
    THIRD   = '-'

grid_size  = 10
grid_value = gameGrid = [[x for x in range(grid_size)] for x in range(grid_size)]
def show_game(grid_value, grid_size):
    print("\n")
    print('     ', end='')
    for i in range(grid_size):
        # Print the top row indicate the horizontal index
        print('  ' + str(i + 1) + '   ', end='')
    for i in range(grid_size):
        print()
        print('    ' + '------' * grid_size + '-')
        print(' ' + str(i + 1) + (' |' if i > 8 else '  |'), end='')
        for j in range(grid_size):
            print('  ' + str(grid_value[i][j]) + '  |', end='')
    
    print()
    # The bottom line
    print('    ' + '------' * grid_size + '-')

# show_game(grid_value, grid_size)
values = [item.value for item in Color]

print(Color.FIRST.value)
