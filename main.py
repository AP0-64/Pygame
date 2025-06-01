import numpy as np
import pretty_midi as pm
import pygame as pg
import pygame.midi as pgm

pg.init()
pgm.init()

screen = pg.display.set_mode((1080, 1920))
center = np.array([x // 2 for x in screen.get_size()])
diameter = 44
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
        self.position = np.array([500, center[1]], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.note_index = 0
        self.note_end_time = 0
        self.current_note = None

    def update(self):
        self.velocity[1] += 0.3
        self.position += self.velocity

    def draw(self, screen):
        pg.draw.circle(
            screen,
            (255, 255, 255),
            self.position.astype(int),
            diameter
        )
        pg.draw.circle(screen, (255, 0, 0), self.position.astype(int), 40)

    def bounce(self):
        direction = self.position - center
        distance = np.linalg.norm(direction)
        if distance + diameter >= 300 and distance != 0:
            normal = direction / distance
            self.velocity = (
                self.velocity
                - 2 * np.dot(self.velocity, normal) * normal
            )
            self.position = center + normal * (300 - 44)
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

    screen.fill((0, 0, 0))

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
