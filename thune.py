import pygame as pg

pg.init()

screen = pg.display.set_mode((540, 960))
screen.fill((0, 0, 0))
pg.display.set_caption("Test Pygame")

pg.draw.circle(screen, (255, 255, 255), [270, 480], 44)
pg.draw.circle(screen, (255, 0, 0), [270, 480], 40)

pg.display.flip()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
