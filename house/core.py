import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from house.furniture import X, Bed, Armario
from house.scene import Controls, Camera, Lighting, draw_ground, TextureLoader
import os


class Core:
    base_resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
    # camera vars
    eye = (0, 0, 10)
    target = (0, 0, 0)
    up = (0, 1, 0)

    # light vars
    luz_ambiente = (0.4, 0.4, 0.4, 1.0)
    luz_difusa = (0.7, 0.7, 0.7, 1.0)
    luz_especular = (1.0, 1.0, 1.0, 1.0) # cor da luz especular, 4 valor é transparencia
    posicao_luz = (6, 10, 10, 1.)
    especularidade = (1.0, 1.0, 1.0, 1.0)
    espec_material = 50

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if self.__getattribute__(key):
                self.__setattr__(key, value)

        self.texture_loader = TextureLoader(os.path.join(self.base_resources_path, 'textures'))

        # todo: maybe auto retrieve classes from furnitures module
        # clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        self.furnitures = [
            # X(self.texture_loader),
            Armario(self.texture_loader),
            Bed(self.texture_loader)
        ]

        pygame.init()
        display = (1600, 900)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        # base settings
        glClearColor(0.761, 0.773, 0.824, 1.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_DEPTH_TEST)

        # set perspective
        gluPerspective(45, (display[0] / display[1]), .1, 50.0)

        self.camera = Camera(self.eye, self.target, self.up)
        self.controls = Controls(self.camera)
        self.controls.scene_objects = self.furnitures
        self.lighting = Lighting(
            self.especularidade,
            self.espec_material,
            self.luz_ambiente,
            self.luz_difusa,
            self.luz_especular,
            self.posicao_luz
        )
        self.lighting.set_lighting()

        # ground texture
        self.ground_texture = self.texture_loader.load_texture('ground_texture.png')

    def main_loop(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        self.camera.set_look_at()
        self.lighting.set_lighting_position()

        self.event_capture_loop()

        self.draw_furniture_loop()

        draw_ground(self.ground_texture)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(33)

    def draw_furniture_loop(self):
        for f in self.furnitures:
            glPushMatrix()
            f.draw_on_scene()
            glPopMatrix()

    def event_capture_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                self.controls.handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.controls.orbital_control(event.button)
