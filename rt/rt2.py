import math
import os.path
import numpy as np
from sn.gl import *
from sn.gl.geometry.volume import V as Volume
from sn.gl.geometry.volume import D as Demo
import sn.gl.geometry.t3d as T
from sb03 import *
from random import random

class V(Volume):

    program = None

    def __init__(self, program, S):
        super().__init__(program)

        N = self.N = S * S * S

        vvals = (np.array(range(S)) * 2 / (S - 1) - 1) / 10
        points = [ (x, y, z) for x in vvals for y in vvals for z in vvals ]
        print(points)
        v = np.array(points, dtype=np.float32).flatten()

        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

        position_l = program.a['position_vs'].loc
        glVertexAttribPointer(position_l, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position_l)
        self.unbind()

    def render(self):
        super().render()
        glDrawArrays(GL_POINTS, 0, self.N)

class RT2(Demo):

    def initializeGL(self):
        S = 2
        shaderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rt2.shaders')
        super().initializeGL(shaderpath, lambda program: V(program, S))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        self.program.u['pointsize'](30/S)

    def resizeGL(self, w, h):
        super().resizeGL(w, h)

    def paintGL(self):
        super().paintGL()

        program = self.program
        program.use()

        t = Time.time
        program.u['t'](t)
        program.u['color_u']((math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2)

        glDrawArrays(GL_POINTS, 0, 5)
        glFlush()

if __name__ == '__main__':
    RT2.start(RT2)