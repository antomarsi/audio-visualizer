import sys
import pyaudio
import numpy as np
import time
import pygame
from pygame.locals import *

CHUNK = 32
RATE = 44100
WIDTH = 420
HEIGHT = 360
WAVE_HEIGHT_MULTIPLIER = 1
FPS = 60

pygame.font.init()

FPS_FONT = pygame.font.SysFont("Verdana", 20)
GOLDENROD = pygame.Color("goldenrod")



def get_freq_realtive_range(freq, multiplier=1, max_amp=2**16/2, min_amp=-2**16/2):
    freq = freq * multiplier
    return ((freq - min_amp) * 100) / (max_amp - min_amp)


def draw_fps(window, clock):
    fps_overlay = FPS_FONT.render(str(int(clock.get_fps())), True, GOLDENROD)
    window.blit(fps_overlay, (0, 0))


def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=int(RATE),
                    input=True, frames_per_buffer=CHUNK)
    clock = pygame.time.Clock()
    pygame.init()
    scrsize = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(scrsize, HWSURFACE | DOUBLEBUF)
    # visualizer animation starts here
    running = True
    delta_time = 0
    show_fps = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    show_fps = not show_fps
        samples = int(delta_time * RATE)
        count = 0
        while count < samples:
            stream.read(CHUNK)
            count += CHUNK
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        x_unit = scrsize[0] / (CHUNK-1)
        screen.fill([0, 0, 0])
        points = []
        for index, freq in enumerate(data):
            value = get_freq_realtive_range(freq, WAVE_HEIGHT_MULTIPLIER)
            pointX = int(index*x_unit)
            pointY = int(scrsize[1] * (value/100))
            points.append([pointX, pointY])
        pygame.draw.lines(screen, [0, 255, 0], False, points, 1)
        if show_fps:
            draw_fps(screen, clock)
        pygame.display.flip()
        delta_time = clock.tick(FPS)/1000
    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()