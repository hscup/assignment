import pygame


# Cell block size determines how big each square grid block is
BLOCK_SIZE = 90

class Car(pygame.sprite.Sprite):
    """
    Car sprite super class. Contains class variables that all cars should have: orientation, size, and position
    """

    def __init__(self, orientation, size, row, col):
        """
        Constructor
        """
        super(Car, self).__init__()
        self.orientation = orientation
        self.block_size = BLOCK_SIZE
        self.size = size * self.block_size
        self.x = col * self.block_size
        self.y = row * self.block_size


class TargetCar(Car):
    """
    The car which users must move to the target destination in order to win
    """

    def __init__(self, orientation, size, row, col):
        """
        Constructor
        """
        Car.__init__(self, orientation, size, row,
                     col)  # calls superclass init
        # assigns an image to the instance
        self.image = pygame.image.load('images/target.png')
        # assigns a rectangle the size of red car
        self.rect = pygame.Rect(self.x, self.y, self.size, BLOCK_SIZE)


class OtherCar(Car):
    """
    The other vehicles obstructing the red car's path. They can either be of length 2 or 3
    with either a vertical or horizontal orientation
    """

    def __init__(self, orientation, size, row, col):
        """
        Constructor
        """
        Car.__init__(self, orientation, size, row, col)
        if orientation == 'h':  # assigns images and rectangles for horizontal cars
            self.rect = pygame.Rect(
                self.x, self.y, self.size, self.block_size)
            if size == 2:
                self.image = pygame.image.load('images/h2.png')
            elif size == 3:
                self.image = pygame.image.load('images/h3.png')
        else:  # assigns images and rectangles for vertical cars
            self.rect = pygame.Rect(
                self.x, self.y, self.block_size, self.size)
            if size == 2:
                self.image = pygame.image.load('images/v2.png')
            elif size == 3:
                self.image = pygame.image.load('images/v3.png')