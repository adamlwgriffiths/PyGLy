from ctypes import string_at

from pyglet.gl import *

profiles = [
    'legacy',
    'core'
    ]

profile = None
version = None
major_version = None
minor_version = None
glsl_version = None
glsl_major_version = None
glsl_minor_version = None

def _extract_version(version):
    import re
    # version is guaranteed to be 'MAJOR.MINOR<XXX>'
    # there can be a 3rd version
    # split full stops and spaces and take the first 2 results
    versions = re.split( r'[\.\s\-]', version )
    return versions[ 0 ], versions[ 1 ]


def gl_version():
    return gl_info.get_version()

def gl_version_tuple():
    return extract_version(
        gl_info.get_version()
        )

def gl_profile():
    major, minor = version_tuple()
    if major <= 2:
        return 'legacy'
    else:
        return 'core'

def glsl_version():
    return string_at(
        glGetString( GL_SHADING_LANGUAGE_VERSION )
        )

def glsl_version_tuple():
    return extract_version( glsl_version() )

def is_legacy():
    return gl_info.have_version( major = 1 )

def is_core():
    return gl_info.have_version( major = 3 )

def print_gl_info():
    print "OpenGL version:", gl_version()
    print "GLSL version:", glsl_version()
