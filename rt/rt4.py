import locale

from ctypes import *
import sys
from time import time
from random import random
# from sb03 import *

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.t3d as T

import sn.gl.debug

sn.gl.debug.logOnShaderVariables(True)

class RT4(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False
        s = self.S = 200
        self.points = points = [((random()**2 - 0.5) * 4, (random()**2 * 0.8 + 0.2) * 5, (i*10.0)/(s**3)) for i in range(s ** 3)]
        # self.delays = np.arange(125 * 2) / 249.0 * 3.0

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('rt4.shaders', lambda program: Points(program, points))

        """
        self.geometry.bind()
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, self.delays.nbytes, self.delays, GL_STATIC_DRAW)

        delay_l = self.program.a['delay'].loc
        glVertexAttribPointer(delay_l, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(delay_l)
        self.geometry.unbind()
        """

        eye, target, up = T.vec3(0, 0, 30), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        #for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
        glDisable(GL_DEPTH_TEST)
        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](50 / self.S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        super().paintGL()
        t = Time.time % 10.0;
        assert (t >= 0 and t < 10.0)
        self.program.u['t'](t)

if __name__ == '__main__':
    RT4.start(RT4, fullscreen=True)