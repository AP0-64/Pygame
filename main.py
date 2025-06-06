import numpy as np
import pretty_midi as pm
import pygame as pg
import pygame.midi as pgm
import colorsys

pg.init()
pgm.init()

screen = pg.display.set_mode((1080, 1920))
center = np.array([x // 2 for x in screen.get_size()])
pg.display.set_caption("Pygame")

clock = pg.time.Clock()

midi_data = pm.PrettyMIDI("I'm Blue.mid")
all_notes = [
    n
    for inst in midi_data.instruments
    for n in inst.notes
    if n.pitch > 45
]
all_notes.sort(key=lambda n: n.start)
midi_out = pgm.Output(0)


class Ball:
    def __init__(self):
        self.position = np.array([700, 800], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.note_index = 0
        self.note_end_time = 0
        self.current_note = None
        self.trail = []
        self.trail_timer = 0
        self.diameter = 44
        self.hue = 0.0  # de 0.0 à 1.0
        self.hue_step = 0.002  # plus petit = plus lent

    def update(self):
        self.velocity[1] += 0.2
        self.position += self.velocity
        self.trail_timer += 1
        if self.trail_timer % 3 == 0:  # 1 point toutes les 3 frames
            # Capture la couleur actuelle
            r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
            color = (int(r * 255), int(g * 255), int(b * 255))
            self.trail.insert(0, (self.position.copy(), color))

    def draw(self, screen):
        for pos, color in reversed(self.trail):
            # Dessine le contour noir
            pg.draw.circle(
                screen,
                (0, 0, 0),
                pos.astype(int),
                self.diameter // 2 + 2  # un peu plus grand pour liseré noir
            )
            # Dessine la couleur d'origine
            pg.draw.circle(
                screen,
                color,
                pos.astype(int),
                self.diameter // 2
            )
        self.hue += self.hue_step
        if self.hue > 1.0:
            self.hue -= 1.0

    def bounce(self):
        direction = self.position - center
        distance = np.linalg.norm(direction)
        if distance + self.diameter >= 300 and distance != 0:
            normal = direction / distance
            self.velocity = (
                self.velocity
                - 2 * np.dot(self.velocity, normal) * normal
            )
            self.position = center + normal * (300 - self.diameter)
            self.diameter += 1
            if self.note_index < len(all_notes):
                note = all_notes[self.note_index + 21]
                midi_out.note_on(note.pitch, note.velocity)
                self.note_index += 1
                self.note_end_time = pg.time.get_ticks() + 300
                self.current_note = note.pitch


ball = Ball()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    ball.bounce()
    ball.update()
    ball.draw(screen)
    if ball.current_note and pg.time.get_ticks() > ball.note_end_time:
        midi_out.note_off(ball.current_note, 100)
        ball.current_note = None
    pg.draw.circle(screen, (255, 255, 255), center.astype(int), 300, 10)

    pg.display.flip()
    clock.tick(60)

pg.quit()
midi_out.close()
pgm.quit()
