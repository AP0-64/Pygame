import numpy as np
import pygame as pg
import time

pg.mixer.init(frequency=44100, size=-16, channels=1)


def midi_to_freq(midi_note):
    return 440.0 * 2 ** ((midi_note - 69) / 12)


def generate_tone(frequency, duration=0.5, volume=0.5):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * t * 2 * np.pi)
    wave = (wave * 32767 * volume).astype(np.int16)
    sound = pg.sndarray.make_sound(wave)
    return sound


# Exemple d'utilisation:
freq = midi_to_freq(60)  # note C4
sound = generate_tone(freq)
sound.play()
time.sleep(60)
