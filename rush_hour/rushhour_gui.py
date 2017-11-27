import sys

import pygame

from Car import TargetCar, OtherCar, BLOCK_SIZE


class Game:
    """
    Game class contains elements of the rush hour game. Contains class variables and methods for the GUI
    """

    def __init__(self, x, y):
        """
        Constructor
        """
        pygame.init()  # initializes pygame
        self.screen_x = x
        self.screen_y = y
        self.screen = pygame.display.set_mode((x, y))  # sets up display
        pygame.display.set_caption('Rush Hour')
        self.cars = []  # list of car objects
        # assigns the winning block
        # At row 2, column 5
        self.winning_block = pygame.Rect(
            5 * BLOCK_SIZE, 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.clock = pygame.time.Clock()  # for timing control
        self.fps = 60
        self.load_game()  # loads the map from data file

    def load_game(self):
        """
        Loads the game from a puzzle file. First entry in the file is the TargetCar with subsequent entries being the other cars.
        """
        car_infos = []
        with open(sys.argv[1], 'r') as game_file:
            # Read line by line
            for line in game_file:
                car_infos.append([x.strip() for x in line.split(',')])

        # Iterate car in the list
        for index, car in enumerate(car_infos):
            # Get the target car from the first line
            if index == 0:
                car = TargetCar(car_infos[index][0], int(car_infos[index][1]), int(
                    car_infos[index][2]), int(car_infos[index][3]))
            # Other car
            else:
                car = OtherCar(car_infos[index][0], int(car_infos[index][1]), int(
                    car_infos[index][2]), int(car_infos[index][3]))
            self.cars.append(car)

    def display_text(self, display, message, location):
        """
        Display text on the GUI screen
        Params:
            - display: screen which the text is displayed
            - message: text to be displayed
            - location: where the text is displayed on screen
        """
        font = pygame.font.SysFont(None, 48)
        text_to_screen = font.render(message, True, (23,7,243))
        display.blit(text_to_screen, location)

    def update_board(self):
        """
        Draw one car onto screen
        """
        for car in self.cars:
            self.screen.blit(car.image, car.rect)
        pygame.display.update()

    def is_win(self, car):
        """
        Check if the target car is in the winning block
        """
        if car.rect.contains(self.winning_block):
            return True
        return False

    def is_valid_move(self, car, orig_x, orig_y, direction):
        """
        Check if a drag move on a car valid
        """
        # if car doesn't move, return False
        if orig_x == car.rect.x and orig_y == car.rect.y:
            return False

        # The occupied_block rectangle represents the total space occupied by a drag move
        # For example, for a car moving from the very left to the very right in a row,
        # a occupied_block would be a rectangle which takes up that entire row.
        # Horizontal move
        if direction == 'h':
            # Move to left
            if orig_x > car.rect.x:
                occupied_block = pygame.Rect(
                    car.rect.x, car.rect.y, orig_x + car.size - car.rect.x, BLOCK_SIZE)
                # checks if the car is still entirely in the screen
                boundary = 0 <= car.rect.x <= self.screen_x
            # move to right
            else:
                occupied_block = pygame.Rect(
                    orig_x, orig_y, car.rect.x + car.size - orig_x, BLOCK_SIZE)
                boundary = 0 <= car.rect.x + car.size <= self.screen_x
        # vertical move
        else:
            # move down
            if orig_y < car.rect.y:
                occupied_block = pygame.Rect(
                    orig_x, orig_y, BLOCK_SIZE, car.rect.y + car.size - orig_y)
                boundary = 0 <= car.rect.y + car.size <= self.screen_y
            # move up
            else:
                occupied_block = pygame.Rect(
                    car.rect.x, car.rect.y, BLOCK_SIZE, orig_y + car.size - car.rect.y)
                boundary = 0 <= car.rect.y <= self.screen_y

        # Check if car is out of bound
        if not boundary:
            return False

        for i in self.cars:
            if i != car:
                # checks for collisions. If occupied_block collides with any other car, there is a collision
                if occupied_block.colliderect(i.rect):
                    return False
        return True

    def draw_grid(self):
        """
        Draw grid lines to show each block
        """
        # line color
        color = (10, 10, 10)
        # Draw vertical line
        for i in range(0, self.screen_x + 1, BLOCK_SIZE):
            pygame.draw.line(self.screen, color, (i, 0),
                             (i, self.screen_y), 8)
        # Draw horizontal line
        for j in range(0, self.screen_y + 1, BLOCK_SIZE):
            pygame.draw.line(self.screen, color, (0, j),
                             (self.screen_x, j), 8)

    def play(self):
        """
        Handle user input
        """
        self.clock.tick(self.fps)  # set refresh rate
        drag = False  # True if user is dragging a car for a move
        running = True  # True if user has not clicked the quit button
        turn = 0  # counter for number of moves
        car = None
        while running:
            # if self.win, then no longer updates the screen
            if not self.is_win(self.cars[0]):
                self.screen.fill((187, 247, 191))  # fill out the screen
                self.draw_grid()  # then draw the grid
                self.update_board()  # then draw the cars
            # Get user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for win
                elif self.is_win(self.cars[0]):
                    pygame.display.update()
                    self.display_text(self.screen, 'Great! You won in ' + str(turn) +
                                      ' moves', [self.screen_x / 2 - BLOCK_SIZE, self.screen_y / 2])

                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN:  # handles left and right mouse button clicks
                    for i in self.cars:
                        # finds which car is clicked
                        if i.rect.collidepoint(event.pos):
                            car = i
                            drag = True
                            orig_x = car.rect.x
                            orig_y = car.rect.y
                            x, y = event.pos
                            off_x = car.rect.x - x
                            off_y = car.rect.y - y
                elif event.type == pygame.MOUSEBUTTONUP:  # handles left and right mouse button release
                    if not car:
                        break
                    drag = False
                    car.rect.x = round(car.rect.x / BLOCK_SIZE) * \
                        BLOCK_SIZE  # "snaps" the car into grid
                    car.rect.y = round(car.rect.y / BLOCK_SIZE) * BLOCK_SIZE
                    if car.orientation == 'h':
                        # if car is horizontal, its final y should equal its initial y
                        if car.rect.y == orig_y and self.is_valid_move(car, orig_x, orig_y, 'h'):
                            turn += 1  # then checks if the move is legal.
                        else:  # if moved sideways or not legal, car goes back to its original location
                            car.rect.x = orig_x
                            car.rect.y = orig_y
                    else:  # if car is vertical, its final and initial x should be the same, then checks if move is legal.
                        if car.rect.x == orig_x and self.is_valid_move(car, orig_x, orig_y, 'v'):
                            turn += 1
                        else:  # moves car back to original location
                            car.rect.x = orig_x
                            car.rect.y = orig_y

                elif event.type == pygame.MOUSEMOTION:  # handles mouse movenements
                    if drag:  # if a car has been clicked and is being dragged
                        x, y = event.pos
                        car.rect.x = x + off_x
                        car.rect.y = y + off_y

            # displays the number of legal moves user has made.
            self.display_text(self.screen, 'moves: ' + str(turn), [0, 0])
            pygame.display.update()  # updates the display surface


def main():
    # Our board is 6x6
    screen_length = 6 * BLOCK_SIZE
    screen_width = 6 * BLOCK_SIZE
    rush_hour = Game(screen_length, screen_width)
    rush_hour.play()


if __name__ == '__main__':
    main()
