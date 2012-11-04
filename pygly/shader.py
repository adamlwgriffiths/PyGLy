"""Provides Shader and ShaderProgram classes.

Example usage:

shaders = {
    'vert': '''
    VERTEX SHADER TEXT GOES HERE
    ''',

    'frag': '''
    FRAGMENT SHADER TEXT GOES HERE
    ''',
    }

# compile and attach our shaders but don't link
# the program just yet
shader = ShaderProgram(
    False,
    Shader( GL_VERTEX_SHADER, shaders['vert'] ),
    Shader( GL_FRAGMENT_SHADER, shaders['frag'] )
    )
# bind our vertex attributes
shader.attribute( 0, 'in_position' )
shader.attribute( 1, 'in_normal' )
shader.attribute( 2, 'in_colour' )
# bind our fragment output
shader.frag_location( 'out_frag_colour' )
# link the shader
shader.link()

# set any values that don't change
shader.bind()
shader.uniformi( 'in_texture_0', 0 )
shader.unbind()

# do some other things

shader.bind()
# set our per-frame uniforms
shader.uniformf( 'time', 1.0 )

# render some geometry

shader.unbind()
"""

from ctypes import *
import types
import re

from pyglet.gl import *


def parse_shader_error( error ):
    """Parses a single GLSL error and extracts the line number
    and error description.

    Line number and description are returned as a tuple.

    GLSL errors are not defined by the standard, as such,
    each driver provider prints their own error format.

    Nvidia print using the following format:
    0(7): error C1008: undefined variable "MV"

    ATi and Intel print using the following format:
    ERROR: 0:131: '{' : syntax error parse error
    """
    # Nvidia
    # 0(7): error C1008: undefined variable "MV"
    match = re.match( r'(\d)\((\d+)\):\s(.*)', error )
    if match:
        return (
            int(match.group( 2 )),   # line number
            match.group( 3 )    # description
            )

    # ATI
    # Intel
    # ERROR: 0:131: '{' : syntax error parse error
    match = re.match( r'ERROR:\s(\d+):(\d+):\s(.*)', error )
    if match:
        return (
            int(match.group( 2 )),   # line number
            match.group( 3 )    # description
            )

    raise ValueError( 'Unknown GLSL error format' )

def parse_shader_errors( errors ):
    """Parses a GLSL error buffer and returns an list of
    error tuples.
    """
    results = []
    error_list = errors.split( '\n' )
    for error in error_list:
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

    @classmethod
    def create_from_existing( cls, type, content, handle ):
        """Creates a Shader object using an existing shader handle
        """
        obj = cls( type, content, False )
        obj.handle = handle
        return obj

    def __init__( self, type, content, compile_now = True ):
        super( Shader, self ).__init__()

        self.type = type
        self.content = content
        self._handle = None

        if compile_now:
            self.compile()

    def __del__( self ):
        try:
            # del can be called when our modules have been torn down
            # we can try our best to get access to this method
            # but it may still throw an exception
            from pyglet.gl import glDeleteShader

            # mark our shader for deletion
            handle = getattr( self, '_handle', None )
            if handle:
                glDeleteShader( handle )
        except ImportError:
            pass

    @property
    def handle( self ):
        return self._handle

    @handle.setter
    def handle( self, handle ):
        # free our existing handle
        if self._handle:
            glDeleteShader( self._handle )
        self._handle = handle

    def compile( self ):
        """Compiles the shader using the current content
        value.

        This is required before a ShaderProgram is linked.

        This is not required to be performed in order to
        attach a Shader to a ShaderProgram. As long as the
        Shader is compiled prior to the ShaderProgram being
        linked.
        """
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
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        # print the log to the console
        errors = parse_shader_errors( buffer )
        content = self.content.split('\n')

        for error in errors:
            line, desc = error

            print """Error compiling shader type: %s
\tLine: %i
\tDescription: %s
\tCode: %s""" % (
            Shader.types[ self.type ],
            line,
            desc,
            content[ line - 1 ]
            )

    def check_for_errors( self ):
        """Checks for any errors in the shader.

        This is called automatically by the compile method.

        Prints any errors to the console.
        Returns False if an error is set, otherwise True.
        """
        # retrieve the compile status
        value = c_int(0)
        glGetShaderiv( self.handle, GL_COMPILE_STATUS, byref(value) )

        # if compilation failed, print the log
        if not value:
            # retrieve the log length
            glGetShaderiv( self.handle, GL_INFO_LOG_LENGTH, byref( value ) )

            # retrieve the log text
            buffer = create_string_buffer( value.value )
            glGetShaderInfoLog( self.handle, value, None, buffer )

            # print the errors
            self.print_errors( buffer.value )

            # free our shader
            glDeleteShader( self.handle )
            self.handle = None

            return False

        return True



class ShaderProgram( object ):
    """Defines a complete Shader Program, consisting of at least
    a vertex and fragment shader.
    
    Shader objects are decoupled from ShaderPrograms to avoid recompilation
    when re-using shaders.

    Multiple shaders of the same type can be attached together.
    This lets you combine multiple smaller shaders into a single larger one.
    """
    
    def __init__( self, link_now = True, *args ):
        # create the program handle
        self._handle = glCreateProgram()

        for shader in args:
            self.attach_shader( shader )

        if link_now:
            self.link()

    def __del__( self ):
        # del can be called when our modules have been torn down
        # we can try our best to get access to this method
        # but it may still throw an exception
        try:
            from pyglet.gl import glDeleteProgram

            handle = getattr( self, '_handle', None )
            if handle:
                glDeleteProgram( handle )
        except ImportError:
            pass

    @property
    def handle( self ):
        return self._handle

    @handle.setter
    def handle( self, handle ):
        # free our existing handle
        if self._handle:
            glDeleteProgram( self._handle )
        self._handle = handle

    def attach_shader( self, shader ):
        """Attaches a Shader object for the specified GL_*_SHADER type.

        This expects an instance of the Shader class (or equivalent).
        If you need to attach a normal GL shader handle, use the
        Shader.create_from_existing class method to instantiate a
        Shader object first.
        """
        try:
            # attach the shader
            glAttachShader( self.handle, shader.handle )
        except Exception as e:
            print """Error attaching shader type: %s
\tException: %s
""" % (
                Shader.types[ shader.type ],
                str(e)
                )
            # chain the exception
            raise

    def print_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        print """Error linking shader:
\tDescription: %s""" % ( buffer )

    def check_for_errors( self ):
        """Checks for any errors in the program.

        This is called automatically by the link method.

        Prints any errors to the console.
        Returns False if an error is set, otherwise True.
        """
        # retrieve the link status
        value = c_int(0)
        glGetProgramiv( self.handle, GL_LINK_STATUS, byref(value) )

        # if linking failed, print the log
        if not value:
            # retrieve the log length
            glGetProgramiv( self.handle, GL_INFO_LOG_LENGTH, byref(value) )

            # retrieve the log text
            buffer = create_string_buffer( value.value )
            glGetProgramInfoLog( self.handle, value, None, buffer )

            # print the errors
            self.print_errors( buffer.value )

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
        """Binds the shader program to be the active shader program.

        The shader MUST be linked for this to be valid.

        It is valid to bind one shader after another without calling
        unbind.
        """
        # bind the program
        glUseProgram( self.handle )

    def unbind(self):
        """Unbinds the shader program.

        This sets the current shader to null.

        It is valid to bind one shader after another without calling
        unbind.
        Be aware that this will NOT unwind the bind calls.
        Calling unbind will set the active shader to null.
        """
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

        This program must be currently bound.
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

