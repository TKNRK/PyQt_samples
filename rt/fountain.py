import inspect, math, os.path

from sn.qt import *
from sn.gl import *
import sn.gl.geometry.t3d as T

import sn.gl.debug
debug.logOnSetUniform(True)

from sn.gl.geometry.pointgrid import V as PointGrid
from sn.gl.geometry.volume import D as DemoWidget

import 

class RTWidget(DemoWidget):
    def initializeGL(self):

        self.velocity = 0.0
        self.theta = 0.0
        self.phi = 0.0
        self.data = GLfloat[nParticles * 3]
        self.v = T.vec3(0.0,0.0,0.0)

        for i in range(nParticles):
            # Pick the direction of the velocity
            theta = glm::mix(0.0, (float)PI / 6.0, randFloat())
            phi   = glm::mix(0.0, (float)TWOPI, randFloat())

            v.x = math.sin(theta) * math.cos(phi)
            v.y = math.cos(theta)
            v.z = math.sin(theta) * math.sin(phi)

            # Scale to set the magnitude of the velocity (speed)
            velocity = glm::mix(1.25, 1.5, randFloat())
            v = v * velocity

            data[3*i]   = v.x
            data[3*i+1] = v.y
            data[3*i+2] = v.z

        glBindBuffer(GL_ARRAY_BUFFER, startTime)
        glBufferSubData(GL_ARRAY_BUFFER,0,nParticles*sizeof(float), data)

        S = 80
        super().initializeGL('fountain.shaders', lambda program: PointGrid(program, S))

        self.eye = T.homogeneous(T.vec3(0.2, 1.1, 1.2))
        self.target, self.up = T.vec3(0.5, 0.6, 0.7), T.vec3(0, 1, 0)

        self.program.u['pointsize'](800/S)
        self.program.u['ParticleLifetime'](10.0)
        self.program.a['VertexInitVel'](0.0,0.0,0.0)
    
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    def paintGL(self):
        data = GLfloat[nParticles]
        time = 0.0
        rate = 0.00075
        for i in range(nParticles):
            data[i] = time
            time += rate
        glBindBuffer(GL_ARRAY_BUFFER, startTime)
        glBufferSubData(GL_ARRAY_BUFFER,0,nParticles*sizeof(float), data)

        super().paintGL()

    def onTick(self):
        debug.logOnSetUniform(False)
        self.updateGL()

RTWidget.start(RTWidget, fullscreen=True)