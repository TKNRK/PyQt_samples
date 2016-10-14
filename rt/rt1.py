import math
from sb03 import *
from random import random

class W(SB03):
    program = None

    def initializeGL(self):
        super().initializeGL()
        self.program = self.program or Program('rt1.shaders')
        self.va = VertexArray()
        glPointSize(10)

    def paintGL(self):
        super().paintGL()

        program = self.program
        program.use()

        self.va.bind()

        t = Time.time
        program.a['VertexInitVel'](0.03, 0.1, 0.0)
        program.u['t'](t)
        program.u['color_u']((math.cos(t) + 1) / 2, (math.sin(t) + 1) / 2)

        glDrawArrays(GL_POINTS, 0, 3)
        glFlush()

if __name__ == '__main__': start(W)
