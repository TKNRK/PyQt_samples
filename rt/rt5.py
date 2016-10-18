import locale

from ctypes import *
import sys
from time import time
from random import random
from sb03 import *

from PyQt5 import QtCore, QtGui
from sn.gl import *
from sn.qt import *
from sn.gl.geometry.volume import D as Demo
from sn.gl.geometry.points import V as Points
import sn.gl.geometry.t3d as T

import sn.gl.debug

sn.gl.debug.logOnShaderVariables(True)

class RT5(Demo):

    def __init__(self, W):
        super().__init__(W)
        self.should_handle_mouse_click = False
        s = self.S = 5
        self.points = points = [(0.0,3.0,0.0),(1.0,2.0,1.0),(2.0,1.0,2.0)]

    def minimumSizeHint(self): return QtCore.QSize(600, 600)

    def onTick(self): self.updateGL()

    keyPressEvent = Window.keyPressEvent

    def initializeGL(self):
        points = self.points
        super().initializeGL('rt5.shaders', lambda program: Points(program, points))

        eye, target, up = T.vec3(0, 0, 50), T.vec3(0, 0, 0), T.vec3(0, 1, 0)
        self.View = T.lookat(eye, target, up)

        for p in [GL_VERTEX_PROGRAM_POINT_SIZE, GL_BLEND]:
            glEnable(p)
        self.program.u['pointsize'](100 / self.S)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        super().paintGL()
        t = Time.time % 3.0;
        assert (t >= 0 and t < 3.0)
        self.program.u['t'](t)

if __name__ == '__main__':
    RT5.start(RT5)