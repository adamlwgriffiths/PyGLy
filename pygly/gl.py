from OpenGL.arrays.vbo import VBO
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL import *


def _extract_version(version):
    import re
    # version is guaranteed to be 'MAJOR.MINOR<XXX>'
    # there can be a 3rd version
    # split full stops and spaces and take the first 2 results
    versions = re.split( r'[\.\s\-]', version )
    return versions[ 0 ], versions[ 1 ]

def gl_version():
    return glGetString( GL_VERSION )

def gl_version_tuple():
    return _extract_version( gl_version() )

def gl_profile():
    major, minor = gl_version_tuple()
    if major <= 2:
        return 'legacy'
    else:
        return 'core'

def glsl_version():
    return glGetString( GL_SHADING_LANGUAGE_VERSION )

def glsl_version_tuple():
    return _extract_version( glsl_version() )

def is_legacy():
    return gl_version_tuple()[ 0 ] <= 2

def is_core():
    return gl_version_tuple()[ 0 ] >= 3

def print_gl_info():
    print "OpenGL Information:"
    for prop in ["GL_VENDOR", "GL_RENDERER", "GL_VERSION", "GL_SHADING_LANGUAGE_VERSION"]:
        print "\t%s = %s" % (prop, glGetString(globals()[prop]))
