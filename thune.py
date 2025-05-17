import numpy as np
import pygame as pg

pg.init()

screen = pg.display.set_mode((960, 960))  # 540 * 960 px
pg.display.set_caption("Test Pygame")

clock = pg.time.Clock()


class Ball:
    def __init__(self):
        self.ball_position = [480, 480]
        self.ball_velocity = [0, 0]

    def update(self):
        self.ball_velocity[1] += 0.3
        self.ball_position[0] += self.ball_velocity[0]
        self.ball_position[1] += self.ball_velocity[1]

    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255), self.ball_position, 44)
        pg.draw.circle(screen, (255, 0, 0), self.ball_position, 40)


ball = Ball()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    """ if np.linalg.norm(ball.ball_position - [480, 480]) + 44 >= 310:
        pass """

    ball.update()

    pg.draw.circle(screen, (255, 255, 255), [480, 480], 300, 10)
    ball.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()
