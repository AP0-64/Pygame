import pygame as pg

pg.init()

screen = pg.display.set_mode((540, 960))
pg.display.set_caption("Test Pygame")

TOTAL_FRAMES = 60 * 61


class Balle:
    def __init__(self):
        self.ball_position = [270, 480]
        self.ball_velocity = [0, 0]

    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255), self.ball_position, 44)
        pg.draw.circle(screen, (255, 0, 0), self.ball_position, 40)


balle = Balle()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    balle.draw(screen)
    pg.display.flip()

pg.quit()
