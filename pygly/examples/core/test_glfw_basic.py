import glfw

from OpenGL.GL import *

glfw.Init()

glfw.OpenWindowHint( glfw.OPENGL_VERSION_MAJOR, 3);
glfw.OpenWindowHint( glfw.OPENGL_VERSION_MINOR, 2)
glfw.OpenWindowHint( glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.OpenWindowHint( glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

glfw.OpenWindow(
    800, 600,
    8, 8, 8,
    8, 24, 0,
    glfw.WINDOW
    )

glfw.SetWindowTitle( "GLFW" )

def run():
    while True:
        if glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS:
            break

        draw()
        
        glfw.SwapBuffers()

def draw():
    glClearColor( 0.5, 0.5, 0.5, 1.0 )
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )


print glGetString( GL_VERSION )

run()

glfw.Terminate()