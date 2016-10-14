import locale

from ctypes import *
import sys
from time import time
from sb03 import *

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.t3d as T

import sn.gl.debug


sn.gl.debug.logOnShaderVariables(True)


class RT3(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False

        s = self.S = 5
        vvals = np.array(range(s)) * 2. / (s - 1) - 1.
        self.points = points = [(x, y, z) for x in vvals for y in vvals for z in vvals]

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('rt3.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 3), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_CLIP_PLANE0, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](800 / self.S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        super().paintGL()
        t = Time.time
        self.program.u['t'](t)

if __name__ == '__main__':
    RT3.start(RT3)