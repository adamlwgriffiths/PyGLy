#
# Copyright Tristam Macdonald 2008.
#
# Distributed under the Boost Software License, Version 1.0
# (see http://www.boost.org/LICENSE_1_0.txt)
#

from ctypes import *
import types
import re

from pyglet.gl import *


def parse_shader_error( error ):
    # Nvidia
    # 0(7): error C1008: undefined variable "MV"
    match = re.match( '(\\d)\\((\\d+)\\):\\s(.*)', error )
    if match:
        return (
            match.group( 1 ),   # line number
            match.group( 2 )    # description
            )

    # ATI
    # Intel
    # ERROR: 0:131: '{' : syntax error parse error
    match = re.match( 'ERROR:\\s(\\d+):(\\d+):\\s(.*)', error )
    if match:
        return (
            match.group( 1 ),   # line number
            match.group( 2 )    # description
            )

    raise ValueError( 'Unknown GLSL error format' )

def parse_shader_errors( errors ):
    results = []
    for error in errors:
        try:
            result = parse_shader_error( error )
            results.append( result )
        except ValueError as e:
            pass
    return results


class Shader( object ):
    """An individual Shader object.

    Used as part of a single ShaderProgram object.

    A vertex shader (GL_VERTEX_SHADER) and a fragment shader (GL_FRAGMENT_SHADER)
    must be used as part of a single Shader Program.
    Geometry shaders (GL_GEOMETRY_SHADER) are optional.

    Shaders can be used by multiple ShaderPrograms.
    """

    types = {
        GL_VERTEX_SHADER:   'GL_VERTEX_SHADER',
        GL_FRAGMENT_SHADER: 'GL_FRAGMENT_SHADER',
        GL_GEOMETRY_SHADER: 'GL_GEOMETRY_SHADER',
        }

    def __init__( self, type, content, compile_now = True ):
        super( Shader, self ).__init__()

        self.type = type
        self.content = content
        self.handle = None

        if compile_now:
            self.compile()

    def __del__( self ):
        # mark our shader for deletion
        handle = getattr( self, 'handle', None )
        if handle:
            glDeleteShader( handle )

    def compile( self ):
        self.handle = glCreateShader( self.type )

        # convert to c-string
        count = len( self.content )
        src = (c_char_p * count)(*self.content)

        glShaderSource(
            self.handle,
            count,
            cast( pointer(src), POINTER(POINTER(c_char)) ),
            None
            )

        # compile the shader
        glCompileShader( self.handle )

        return self.check_for_errors()

    def print_errors( self, buffer ):
        # print the log to the console
        errors = parse_shader_errors( buffer )
        for error in errors:
            line, desc = error

            print desc
            print self.content[ line - 1 ]

        #print 'Original output:'
        #print buffer.value

    def check_for_errors( self ):
        # retrieve the compile status
        value = c_int(0)
        glGetShaderiv( self.handle, GL_COMPILE_STATUS, byref(value) )

        # if compilation failed, print the log
        if not value:
            # retrieve the log length
            glGetShaderiv( self.handle, GL_INFO_LOG_LENGTH, byref( value ) )

            # retrieve the log text
            buffer = create_string_buffer( value.value )
            glGetShaderInfoLog( handle, value, None, buffer )

            print 'Error compiling shader %s', Shader.types[ self.type ]
            self.print_errors( buffer.value )

            # free our shader
            glDeleteShader( self.handle )
            self.handle = None

            return False

        return True



class ShaderProgram( object ):
    """
    Shader objects are decoupled from ShaderPrograms to avoid recompilation
    when re-using shaders.

    Multiple shaders of the same type can be attached together.
    This lets you combine multiple smaller shaders into a single larger one.

    Example usage:

    shaders = {
        'vert': '''
        VERTEX SHADER TEXT GOES HERE
        ''',

        'frag': '''
        FRAGMENT SHADER TEXT GOES HERE
        ''',
        }

    vert = Shader( GL_VERTEX_SHADER, shaders['vert'] )
    vert.compile()

    frag = Shader( GL_FRAGMENT_SHADER, shaders['frag'] )
    frag.compile()

    shader = ShaderProgram()
    # attach our shaders
    shader.attach_shader( vert )
    shader.attach_shader( frag )
    # bind our vertex attributes
    shader.attribute( 0, 'in_position' )
    shader.attribute( 1, 'in_normal' )
    shader.attribute( 2, 'in_colour' )
    # bind our fragment output
    shader.frag_location( 'out_frag_colour' )
    # link the shader
    shader.link()

    shader.bind()
    # set our per-frame uniforms
    shader.uniformf( 'time', 1.0 )

    # render some geometry

    shader.unbind()

    """
    
    # vert, frag and geom take arrays of source strings
    # the arrays will be concattenated into one string by OpenGL
    def __init__( self, link_now = True, *args ):
        # create the program handle
        self.handle = glCreateProgram()

        for shader in args:
            self.attach_shader( shader )

        if link_now:
            self.link()

    def __del__( self ):
        program = getattr( self, 'program', None )
        if program:
            glDeleteProgram( program )

    def attach_shader( self, shader ):
        """Attaches a Shader object for the specified GL_*_SHADER type.

        This can use both a shader object or a GL shader handle.
        If an object instance is passed in, the GL shader handle will
        be extracted as shader.handle.
        Otherwise, the shader arguement itself will be used as the handle.
        """
        handle = shader
        # check if we've been passed a GL integer or a python object
        if not isinstance( shader, types.IntType ):
            handle = shader.handle

        # attach the shader
        glAttachShader( self.handle, handle )

    def check_for_errors( self ):
        """Checks for any errors in the program.

        Prints any errors to the console.
        Returns False if an error is set, otherwise True.
        """
        # retrieve the link status
        value = c_int(0)
        glGetProgramiv( self.handle, GL_LINK_STATUS, byref(value) )

        # if linking failed, print the log
        if not value:
            # retrieve the log
            # retrieve the log length
            glGetProgramiv( self.handle, GL_INFO_LOG_LENGTH, byref(value) )
            # create a buffer for the log
            buffer = create_string_buffer( value.value )
            # get the buffer
            glGetProgramInfoLog( self.handle, value, None, buffer )

            # print the log to the console
            print "Failed to link shader"
            print buffer.value

            return False

        return True

    def attribute( self, index, name ):
        """Binds the vertex attribute in the specified index to the
        given name used in the shader.

        Attribute locations MUST be bound BEFORE linking
        or the location will not take effect until
        the shader is linked again!

        http://www.opengl.org/sdk/docs/man3/xhtml/glBindAttribLocation.xml
        """
        glBindAttribLocation( self.handle, index, name )

    def frag_location( self, name, buffers = 0 ):
        """Sets the fragment output name used within the program.

        Buffers is the number of buffers receiving the fragment output.
        By default, this is 0.

        Frag data locations MUST be bound BEFORE linking
        or the location will not take effect until
        the shader is linked again!

        http://www.opengl.org/sdk/docs/man3/xhtml/glBindFragDataLocation.xml
        """
        glBindFragDataLocation( self.handle, buffers, name )

    def link(self):
        """Links the specified shader into a complete program.

        It is important to set any attribute locations and
        the frag data location BEFORE calling link or these calls
        will not take effect.
        """
        # link the program
        glLinkProgram( self.handle )
        return self.check_for_errors()

    def bind(self):
        # bind the program
        glUseProgram( self.handle )

    def unbind(self):
        # unbind the
        glUseProgram( 0 )

    def uniformf(self, name, *vals):
        """Upload a floating point uniform.

        This program must be currently bound.
        """
        # check there are 1-4 values
        length = len( vals )
        if length not in range( 1, 5 ):
            raise ValueError( 'Incorrect number of values for uniformf' )

        # retrieve the uniform location
        loc = glGetUniformLocation( self.handle, name )

        # select the correct function
        func = {
            1:  glUniform1f,
            2:  glUniform2f,
            3:  glUniform3f,
            4:  glUniform4f
            }[ length ]

        func( loc, *vals )

    def uniformi(self, name, *vals):
        """Upload an integer uniform.

        This program must be currently bound.
        """
        # check there are 1-4 values
        length = len( vals )
        if length not in range( 1, 5 ):
            raise ValueError( 'Incorrect number of values for uniformi' )

        # retrieve the uniform location
        loc = glGetUniformLocation( self.handle, name )

        # select the correct function
        func = {
            1:  glUniform1i,
            2:  glUniform2i,
            3:  glUniform3i,
            4:  glUniform4i
            }[ length ]

        func( loc, *vals )

    def uniform_matrixf(self, name, mat):
        """Upload a uniform matrix.

        Works with matrices stored as lists, as well as euclid matrices
        """
        # we support 2x2, 3x3, 4x4
        length = len( mat )
        if length not in (4, 8, 16):
            raise ValueError( 'Incorrect number of values for uniform_matrixf' )

        # obtian the uniform location
        loc = glGetUniformLocation( self.handle, name )

        # uplaod the 4x4 floating point matrix
        func = {
            4:  glUniformMatrix2fv,
            8:  glUniformMatrix3fv,
            16: glUniformMatrix4fv,
            }[ length ]

        func( loc, 1, False, (c_float * length)(*mat) )

