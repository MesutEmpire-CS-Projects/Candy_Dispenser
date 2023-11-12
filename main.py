import random

import pygame

from stack import ArrayStack, Empty

import threading

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
CANDY_SIZE = (90, 35)
SPRING_WIDTH = 50
SPRING_HEIGHT = (HEIGHT * 3 / 4 - 40)
EXTENSION = CANDY_SIZE[1]

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Stack Dispenser")
font = pygame.font.Font('freesansbold.ttf', 20)

# Initialize the Stack
candy_stack = ArrayStack()
# candy_stack = LinkedStack()

class Button:
    def __init__(self, name, x, y):
        self._name = name
        self._width = 150
        self._height = 50
        self._rect = pygame.rect.Rect(x, y, self._width, self._height)
        self._enabled = True

    def draw(self):
        pygame.draw.rect(screen, 'black', self._rect, 2)
        text = font.render(self._name, True, 'black')
        screen.blit(text, (self._rect.centerx - text.get_width() // 2, self._rect.centery - text.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)

    def get_name(self):
        return self._name


class Display:
    def __init__(self):
        self._result = None
        self._color = 'black'

    def show(self):
        text = font.render(str(self._result), True, self._color)
        text_rect = pygame.rect.Rect(750, 100, 50, 100)
        screen.blit(text, text_rect)

    def set_result(self, info, color='black'):
        self._result = info
        self._color = color

    def reset_result(self):
        self._result = None

    def get_result(self):
        return self._result


class Candy:
    def __init__(self):
        self._label = random.randint(0, 1000)
        self._color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, x, y):
        candy_rect = pygame.rect.Rect(x, y, CANDY_SIZE[0], CANDY_SIZE[1])
        pygame.draw.ellipse(screen, self._color, candy_rect)
        text = font.render(str(self._label), True, 'black')
        text_rect = pygame.rect.Rect(x - 40, y + 5, CANDY_SIZE[0], CANDY_SIZE[1])
        screen.blit(text, text_rect)

    def get_candy(self):
        return self._label


class Dispenser:
    class _Spring:
        def __init__(self, x, y):
            self._x = x
            self.y = y
            self.height = SPRING_HEIGHT
            self._top_plate_x = WIDTH // 2 - SPRING_WIDTH * 2

        def draw(self):
            pygame.draw.line(screen, 'black', (self._top_plate_x, self.y),
                             (self._top_plate_x + SPRING_WIDTH * 4, self.y),
                             8)
            image = pygame.image.load('spring.png')
            image = pygame.transform.scale(image, (SPRING_WIDTH, self.height))
            screen.blit(image, (self._x, self.y, 5, self.height))

        def adjust(self, operation):
            if operation == 'push':
                if self.height - EXTENSION >= 25:
                    self.height -= EXTENSION
                    self.y += EXTENSION
            elif operation == 'pop':
                if self.height + EXTENSION > SPRING_HEIGHT:
                    self.height = SPRING_HEIGHT
                else:
                    self.height += EXTENSION
                    self.y -= EXTENSION

        def get_y(self):
            return self.y

        def get_height(self):
            return self.height

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._width = SPRING_WIDTH * 4
        self._height = SPRING_HEIGHT
        self._spring = self._Spring(WIDTH // 2 - SPRING_WIDTH // 2, HEIGHT * 1 / 4)
        self._is_lid_open = False

    def draw(self):
        # Draw dispenser
        pygame.draw.lines(screen, 'black', False, [(self._x, self._y), (self._x, self._y + self._height),
                                                   (self._x + self._width, self._y + self._height),
                                                   (self._x + self._width, self._y)], 2)
        # Draw lid
        if self._is_lid_open:
            pygame.draw.line(screen, 'black', (self._x + 100, self._y - 150), (self._x + self._width, self._y),
                             8)
        else:
            pygame.draw.line(screen, 'black', (self._x, self._y-5), (self._x + self._width, self._y-5),
                             8)

        # Draw Spring
        self._spring.draw()

    def adjust_spring(self, operation):
        self._spring.adjust(operation)

    def get_spring_y(self):
        return self._spring.y

    def get_spring_height(self):
        return self._spring.height

    def open_lid(self):
        self._is_lid_open = True

    def close_lid(self):

        self._is_lid_open = False


dispenser = Dispenser(WIDTH // 2 - SPRING_WIDTH * 2, HEIGHT * 1 / 4)
display_info = Display()

buttons = [Button('Pop', 10, 10), Button('Push', 10, 70), Button('Top', 10, 130), Button('Is Empty', 10, 190),
           Button('Len', 10, 250)]


def add_candy():
    if dispenser.get_spring_height() - EXTENSION >= 25:
        dispenser.open_lid()
        dispenser.adjust_spring('push')
        added_candy = Candy()
        candy_stack.push(added_candy)
        display_info.reset_result()
        threading.Timer(0.5, dispenser.close_lid).start()
    else:
        display_info.set_result("Stack is full", 'red')


def remove_candy():
    try:
        removed_candy = candy_stack.pop()
        if removed_candy is not None:
            dispenser.open_lid()
            dispenser.adjust_spring('pop')
            display_info.set_result(f'Popped : {removed_candy.get_candy()}')
            threading.Timer(0.5, dispenser.close_lid).start()

    except Empty:
        display_info.set_result("Error : Stack is empty", 'red')


def is_empty():
    if candy_stack.is_empty():
        display_info.set_result("Error : Stack is empty", 'red')
    else:
        display_info.set_result("Stack is not empty.")


def get_length():
    display_info.set_result(f"Stack Length : {len(candy_stack)}")


def get_top_candy():
    try:
        top_candy = candy_stack.top()
        display_info.set_result(f"Top Candy Label : {top_candy.get_candy()}")
    except Empty:
        display_info.set_result('Error : Stack is empty', 'red')


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(mouse_position):
                    if button.get_name() == 'Pop':
                        remove_candy()
                    elif button.get_name() == 'Push':
                        add_candy()
                    elif button.get_name() == 'Top':
                        get_top_candy()
                    elif button.get_name() == 'Is Empty':
                        is_empty()
                    elif button.get_name() == 'Len':
                        get_length()

    screen.fill('white')
    # Draw buttons
    for button in buttons:
        button.draw()

    # Draw the dispenser
    dispenser.draw()

    # Draw Display window
    if display_info.get_result():
        display_info.show()

    # Draw the candies in the stack
    x = WIDTH // 2 - CANDY_SIZE[0] // 2
    y = dispenser.get_spring_y() - CANDY_SIZE[1]
    for candy in candy_stack.items:
        candy.draw(x, y)
        y -= CANDY_SIZE[1]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
