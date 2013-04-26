# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:40:11 2013

@author: Jorge
"""
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Window(object):
    def __init__(self, width = 400, height = 400, title = "GL Window"):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
        glutCreateWindow(title)
        glutInitWindowPosition(100, 100)
        glutInitWindowSize(width, height)
        self.setup()
        glutDisplayFunc(self._draw)
        glutIdleFunc(self.idle)
        glutKeyboardFunc(self.onKeyboard)
        glutMouseFunc(self.onMouse)
        
    def setup(self):
        pass

    def _draw(self):
        self.draw()
        glutSwapBuffers()
    
    def draw(self):
        pass
    
    def idle(self):
        pass
    
    def onKeyboard(self, key, x, y):
        pass
        
    def onMouse(self, button, type, x, y):
        pass
    
    def start(self):
        glutMainLoop()
        
if __name__ == '__main__':
    class MyWindow(Window):
        def __init__(self):
            Window.__init__(self)
        def setup(self):
            glClearColor(0, 0, 0, 1)
            
        def draw(self):
            glClear(GL_COLOR_BUFFER_BIT)
            
    a = MyWindow()
    a.start()