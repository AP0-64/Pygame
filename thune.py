import numpy as np
import pretty_midi as pm
import pygame as pg

pg.init()

screen = pg.display.set_mode((960, 960))
center = np.array([x // 2 for x in screen.get_size()])
pg.display.set_caption("Pygame")

clock = pg.time.Clock()

midi_data = pm.PrettyMIDI("I'm Blue.mid")
all_notes = [n for inst in midi_data.instruments for n in inst.notes]
all_notes.sort(key=lambda n: n.start)


class Ball:
    def __init__(self):
        self.position = np.array([center[0], center[1]], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.note_index = 0

    def update(self):
        self.velocity[1] += 0.3
        self.position += self.velocity

    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255), self.position.astype(int), 44)
        pg.draw.circle(screen, (255, 0, 0), self.position.astype(int), 40)

    def bounce(self):
        direction = self.position - center
        distance = np.linalg.norm(direction)
        if distance + 44 > 300 and distance != 0:
            normal = direction / distance
            self.velocity = (
                self.velocity - 2 * np.dot(self.velocity, normal) * normal
            )
            self.position = center + normal * (300 - 44)

            # Jouer la prochaine note
            if self.note_index < len(all_notes):
                note = all_notes[self.note_index]
                print(
                    f"Note jouée : pitch={note.pitch}, "
                    f"vélocité={note.velocity}"
                )
                self.note_index += 1


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
    pg.draw.circle(screen, (255, 255, 255), center.astype(int), 300, 10)

    pg.display.flip()
    clock.tick(60)

pg.quit()
