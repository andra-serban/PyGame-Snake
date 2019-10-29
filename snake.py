import math
import random
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Cube(object):

    def __init__(self, position, direction, color=RED):
        self.position = position
        self.direction = direction
        self.color = color

    def move(self, direction):
        self.direction = direction
        p = list(self.position)
        d = list(direction)
        p[0] += d[0]
        p[1] += d[1]
        self.position = tuple(p)


    def draw(self):
        global width, rows, window
        pygame.draw.rect(window, self.color, (self.position[0] * width / rows, self.position[1] * width / rows, rows, rows))
class Snake(object):

    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position, (1, 0), color)
        self.body.append(self.head)
        self.direction = (1, 0)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.K_LEFT:
                self.direction = (-1, 0)
            if event.type == pygame.K_RIGHT:
                self.direction = (1, 0)
            if event.type == pygame.K_UP:
                self.direction = (0, -1)
            if event.type == pygame.K_DOWN:
                self.direction = (0, 1)

        self.turns[self.head.position] = self.direction
        for index, cube in enumerate(self.body):
            position = cube.position
            dx, dy = cube.direction
            px, py = cube.position
            if dx == -1 and px <= 0:
                cube.position = (rows - 1, py)
            elif dx == 1 and px >= rows - 1:
                cube.position = (0, py)
            elif dy == 1 and py >= rows - 1:
                cube.position = (px, 0)
            elif dy == -1 and py <= 0:
                cube.position = (px, rows - 1)

            if position in self.turns:
                if index == 0:
                    self.turns[position] = self.direction
                turn = self.turns[position]
                cube.move(turn)
            else:
                cube.move(cube.direction)

    def extend(self):
        tail = self.body[-1]
        dx, dy = self.direction
        tx, ty = tail.position
        position = (tx - dx, ty - dy)
        self.body.append(Cube(position, tail.direction))

    def draw(self):

        for cube in self.body:
            cube.draw()

def drawWindow():
    global width, rows, window, snake, apple

    window = pygame.display.set_mode((width, width))
    window.fill(BLACK)
    for y in range(width):
        for x in range(width):
            rrect = pygame.Rect(x * width/rows, y * width/rows, rows, rows)
            pygame.draw.rect(window, WHITE, rrect)
    snake.draw()
    pygame.display.update()

def createApple():
    global rows, snake
    x = y = 0

    return Cube((x, y), (0, 0), GREEN)

def main():
    global width, rows, window, snake, apple
    width = 500
    rows = 20
    window = pygame.display.set_mode((width, width))

    snake = Snake(RED, (10, 10))

    clock = pygame.time.Clock()

    isPlaying = True

    apple = createApple()

    while isPlaying:
        clock.tick(20)

        if snake.body[0].position == apple.position:
            snake.extend()
            apple = createApple()

        snake.move()

        for index in range(len(snake.body)):
            if snake.body[index].position in list(map(lambda z: z.position, snake.body[index + 1:])):
                print('Score: ', len(snake.body))
                isPlaying = False


        drawWindow()

main()
