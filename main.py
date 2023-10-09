import pygame
import random
from stack import Stack, Empty

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
BACKGROUND_COLOR = (255, 255, 255)
CANDY_SIZE = (70, 25)
SPRING_WIDTH = 20
MIN_STACK_CAPACITY = 7
SPRING_HEIGHT = 200
SPRING_CONSTANT = 0.8
CANDY_FORCE = 10

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Spring Stack")
font = pygame.font.Font('freesansbold.ttf', 20)



# Initialize the Stack
candy_stack = Stack()


class Button:
    def __init__(self, name, x, y):
        self.name = name
        self.width = 150
        self.height = 50
        self.rect = pygame.rect.Rect(x, y, self.width, self.height)
        self.enabled = True

    def draw(self):
        pygame.draw.rect(screen, 'black', self.rect, 2)
        text = font.render(self.name, True, 'black')
        screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Candy:
    def __init__(self, color):
        self.color = color

    def draw(self, x, y):
        pygame.draw.ellipse(screen, self.color, (x, y, CANDY_SIZE[0], CANDY_SIZE[1]))


class Dispenser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SPRING_WIDTH * 4
        self.height = SPRING_HEIGHT

    def draw(self):
        pygame.draw.lines(screen, 'black', False, [(self.x, self.y), (self.x, self.y + self.height),
                                                   (self.x + self.width, self.y + self.height),
                                                   (self.x + self.width, self.y)])


class Spring:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = SPRING_HEIGHT
        self.dispenser_x = WIDTH // 2 - SPRING_WIDTH * 2
        self.rect = pygame.Rect(self.x, self.y, SPRING_WIDTH, self.height)

    def draw(self):
        pygame.draw.rect(screen, 'black', self.rect)
        pygame.draw.line(screen, 'black', (self.dispenser_x, self.y), (self.dispenser_x + SPRING_WIDTH * 4, self.y), 3)

    def adjust(self, operation):
        extension = CANDY_FORCE / SPRING_CONSTANT
        if operation == 'push':
            if self.height - extension > 20:
                self.height -= extension
                self.y += extension
            else:
                self.height = 20
        elif operation == 'pop':
            if self.height + extension > SPRING_HEIGHT:
                self.height = SPRING_HEIGHT
            else:
                self.height += extension
                self.y -= extension


spring = Spring(WIDTH // 2 - SPRING_WIDTH // 2, 300)
dispenser = Dispenser(WIDTH // 2 - SPRING_WIDTH * 2, 300)

buttons = [
    Button('Pop', 10, 10),
    Button('Push', 10, 70),
    Button('Top', 10, 130),
    Button('Is Empty', 10, 190),
    Button('Len', 10, 250)
]


def add_candy():
    if not candy_stack.is_empty():
        spring.adjust('push')
    # color = random.choice(CANDY_COLORS)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    candy = Candy(color)
    candy_stack.push(candy)


def remove_candy():
    try:
        candy = candy_stack.pop()
        if candy is not None:
            spring.adjust('pop')
    except Empty:
        print("Cannot remove candy: The container is empty.")


def is_empty():
    return candy_stack.is_empty()


def get_length():
    return len(candy_stack)


def get_top_candy_color():
    try:
        top_candy = candy_stack.top()
        return top_candy.color
    except Empty:
        print('Error : Stack is empty')
        return None


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(mouse_pos):
                    if button.name == 'Pop':
                        remove_candy()
                    elif button.name == 'Push':
                        add_candy()
                    elif button.name == 'Top':
                        top_color = get_top_candy_color()
                        if top_color:
                            print(f"Top Candy Color: {top_color}")
                    elif button.name == 'Is Empty':
                        empty_status = is_empty()
                        if empty_status:
                            print("Error: Stack is empty.")
                        else:
                            print("Stack is not empty.")
                    elif button.name == 'Len':
                        stack_length = get_length()
                        print(f"Stack Length: {stack_length}")

    screen.fill('white')

    # Draw the dispenser
    dispenser.draw()

    # Draw the spring
    spring.rect.height = spring.height
    spring.rect.y = spring.y
    spring.draw()

    # Draw the candies in the stack
    x = WIDTH // 2 - SPRING_WIDTH * 1.7
    y = spring.y - CANDY_SIZE[1]
    for candy in candy_stack.items:
        candy.draw(x, y)
        y -= CANDY_SIZE[1] + 5

    # Draw buttons
    for button in buttons:
        button.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
