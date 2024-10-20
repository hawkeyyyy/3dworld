
from meshes.chunkmesh import ChunkMesh
import glm
import numpy as np

# chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE

# world
WORLD_W, WORLD_H = 10, 3
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty:
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        # empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')

        # fill chunk
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            wx = x + cx
            for z in range(CHUNK_SIZE):
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = wy + 1

        if np.any(voxels):
            self.is_empty = False

        return voxels














































