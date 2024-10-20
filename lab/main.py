import pygame
import moderngl as mgl
import sys
import numpy as np
import glm  
from player import Player
from textures import Textures
from world_objects.chunk import Chunk
from shaderprogram import ShaderProgram
from world import World


class MinecraftEngine:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.running = True

        self._init_pygame()
        self._init_opengl()
        self._load_resources()
        self._setup_controls()
        
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), flags=pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)

    def _init_opengl(self):
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

    def _load_resources(self):
        self.player = Player(self)
        self.textures = Textures(self)
        self.shader_program = ShaderProgram(self)
        if self.textures.texture_0 is None:
            print("Failed to load texture.")
      
        self.world = World(self)

    def _setup_controls(self):
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def _load_shader_code(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self):
        self.player.update()
        self.world.update()
        self.delta_time = self.clock.tick() / 1000.0
        self.shader_program.update()
        self.time = pygame.time.get_ticks() * 0.001
        pygame.display.set_caption(f'{self.clock.get_fps():.0f} FPS')

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1)
        self.world.render()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    engine = MinecraftEngine(1600, 900, "Terrain generation with cubes")
    engine.run()
