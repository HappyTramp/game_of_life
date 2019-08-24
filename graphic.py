import os
from time import sleep, time
from threading import Thread

import pygame as pg
from pygame.locals import *


RESOLUTION = (720, 520)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
DECAL_LENGTH = 20
FPS = 30


class Graphic:
    def __init__(self, gol):
        self.gol = gol
        self.running = True
        self.key_event_occured = False
        self.inspect_next = False
        self.full_screen = False
        self.x_decal = 0
        self.y_decal = 0
        self.zoom_level = 0
        self.time_next_draw = time()

    @property
    def square_size(self):
        return self.gol.square_size + self.zoom_level

    def main_loop(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        # display_info = pg.display.Info()
        # self.screen_size = (display_info.current_w, display_info.current_h)
        # print(RESOLUTION == self.screen_size)
        pg.display.set_caption('Game of life')
        self.window = pg.display.set_mode(RESOLUTION, RESIZABLE | DOUBLEBUF)
        self.sans_font = pg.font.SysFont('sans', 15)
        clock = pg.time.Clock()

        while self.running:
            clock.tick(FPS)
            self.event_handler()
            self.update()
            pg.display.flip()

    def update(self):
        if not self.gol.inspect:
            if not time() >= self.time_next_draw:
                return
            self.time_next_draw = time() + self.gol.time_step

        if self.gol.inspect and not self.key_event_occured:
            return
        self.window.fill(BLACK_COLOR)
        for node in self.gol.alive_nodes:
            node_rect = pg.Rect(10 + self.x_decal + (node.x + 1) * self.square_size,
                                45 + self.y_decal + (node.y + 1) * self.square_size,
                                self.square_size, self.square_size)
            pg.draw.rect(self.window, WHITE_COLOR, node_rect)

        gen_text = self.sans_font.render(str(self.gol.generation_counter),
                                         True, WHITE_COLOR, BLACK_COLOR)
        self.window.blit(gen_text, (10, 35))

        gen_text = self.sans_font.render(str(self.gol.pattern_name),
                                         True, WHITE_COLOR, BLACK_COLOR)
        self.window.blit(gen_text, (10, 10))
        if (self.gol.inspect and self.inspect_next) or not self.gol.inspect:
            self.gol.next_generation()
        if self.gol.generation_counter > self.gol.max_gen:
            self.running = False
        self.key_event_occured = False
        self.inspect_next = False

    def event_handler(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.key_event_occured = True
                # trigger next step in inspect mode
                if event.key == K_RETURN or event.key == K_SPACE:
                    self.inspect_next = True
                # quit
                elif event.key == K_q:
                    self.running = False
                # toggle inspect mode
                elif event.key == K_i:
                    self.gol.inspect = not self.gol.inspect
                # elif event.key == K_F11 or (event.key == K_ESCAPE and self.full_screen):
                #     pg.display.toggle_fullscreen()
                #     if self.window.get_flags() & FULLSCREEN:
                #         pg.display.set_mode(RESOLUTION, RESIZABLE | DOUBLEBUF)
                #     else:
                #         pg.display.set_mode(RESOLUTION, RESIZABLE | DOUBLEBUF | FULLSCREEN)
                # view move
                elif event.key == K_UP:
                    self.y_decal += DECAL_LENGTH
                elif event.key == K_DOWN:
                    self.y_decal -= DECAL_LENGTH
                elif event.key == K_LEFT:
                    self.x_decal += DECAL_LENGTH
                elif event.key == K_RIGHT:
                    self.x_decal -= DECAL_LENGTH
                # zoom
                elif event.key == K_MINUS:
                    self.zoom_level -= 1
                elif event.key == K_EQUALS:
                    self.zoom_level += 1
            elif event.type == VIDEORESIZE:
                pg.display.set_mode(event.size, RESIZABLE | DOUBLEBUF)
