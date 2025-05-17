import numpy as np
import pygame as pg

pg.init()

screen = pg.display.set_mode((960, 960))
center = np.array([x // 2 for x in screen.get_size()])
pg.display.set_caption("Test Pygame")

clock = pg.time.Clock()


class Ball:
    def __init__(self):
        self.position = np.array([center[0], center[1]], dtype=float)
        self.velocity = np.array([0.0, 0.0])

    def update(self):
        self.velocity[1] += 0.3
        self.position += self.velocity

    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255), self.position.astype(int), 44)
        pg.draw.circle(screen, (255, 0, 0), self.position.astype(int), 40)


ball = Ball()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    direction = ball.position - center
    distance = np.linalg.norm(direction)

    if distance + 44 > 300:
        if distance != 0:
            normal = direction / distance
            ball.velocity = (
                ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
            )
            # Pas de perte de vitesse avec la ligne ci-dessous
            ball.position = center + normal * (300 - 44)

    ball.update()

    pg.draw.circle(screen, (255, 255, 255), center.astype(int), 300, 10)
    ball.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()
