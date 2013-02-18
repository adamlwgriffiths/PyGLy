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
shader.attributes.in_position = 0
shader.attributes.in_normal = 1
shader.attributes.in_colour = 2

# bind our fragment output
shader.frag_location( 'out_frag_colour' )

# link the shader
shader.link()

# set any uniform values that don't change each frame
shader.bind()

# uniforms can be accessed directly and a uniform
# object of the correct type will automatically be
# created.
# It is still possible to manually assign them.
# Although there is no advantage to this as the
# verification code performs the same steps.
# here, in_texture_0 will be detected as a sampler
# variable and an object of type UniformSampler
# will be created and assigned to it.
# this allows us to do validation on data passed to the
# shader's uniforms.
shader.uniforms.in_texture_0 = 0

shader.unbind()

# do some other things
# ...

# time to render
# bind the shader
shader.bind()

# set our per-frame uniforms
shader.uniforms.in_time = 1.0

# render some geometry
# ...

# unbind the shader
shader.unbind()
"""

import re

import numpy
from OpenGL.GL import *

from pyrr.utils import parameters_as_numpy_arrays


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

def uniforms( handle ):
    """Returns an iterator for the uniforms of the specified program.

    Each uniform returns a tuple with the following values:
        name, size, type
    Where:
        size is the uniform size in types
        type is the GL enumeration
    """
    # we can't get the uniform directly
    # we have to iterate over the active uniforms and find our
    # uniform match by the name given

    # get number of active uniforms
    num_uniforms = glGetProgramiv( handle, GL_ACTIVE_UNIFORMS )

    for index in range( num_uniforms ):
        name, size, type = glGetActiveUniform( handle, index )
        yield name, size, type

def uniform( handle, name ):
    for uniform in uniforms( handle ):
        _name, _size, _type = uniform

        if _name == name:
            return _name, _size, _type

    # no uniform found
    return None

def enum_to_string( glEnum ):
    return {
        GL_VERTEX_SHADER:       'GL_VERTEX_SHADER',
        GL_FRAGMENT_SHADER:     'GL_FRAGMENT_SHADER',
        GL_GEOMETRY_SHADER:     'GL_GEOMETRY_SHADER',
        GL_FLOAT:               "GL_FLOAT",
        GL_FLOAT_VEC2:          "GL_FLOAT_VEC2",
        GL_FLOAT_VEC3:          "GL_FLOAT_VEC3",
        GL_FLOAT_VEC4:          "GL_FLOAT_VEC4",
        GL_INT:                 "GL_INT",
        GL_INT_VEC2:            "GL_INT_VEC2",
        GL_INT_VEC3:            "GL_INT_VEC3",
        GL_INT_VEC4:            "GL_INT_VEC4",
        GL_UNSIGNED_INT:        "GL_UNSIGNED_INT",
        GL_UNSIGNED_INT_VEC2:   "GL_UNSIGNED_INT_VEC2",
        GL_UNSIGNED_INT_VEC3:   "GL_UNSIGNED_INT_VEC3",
        GL_UNSIGNED_INT_VEC4:   "GL_UNSIGNED_INT_VEC4",
        GL_UNSIGNED_INT_ATOMIC_COUNTER: "GL_UNSIGNED_INT_ATOMIC_COUNTER",
        GL_FLOAT_MAT2:          "GL_FLOAT_MAT2",
        GL_FLOAT_MAT3:          "GL_FLOAT_MAT3",
        GL_FLOAT_MAT4:          "GL_FLOAT_MAT4",
        GL_FLOAT_MAT2x3:        "GL_FLOAT_MAT2x3",
        GL_FLOAT_MAT2x4:        "GL_FLOAT_MAT2x4",
        GL_FLOAT_MAT3x2:        "GL_FLOAT_MAT3x2",
        GL_FLOAT_MAT3x4:        "GL_FLOAT_MAT3x4",
        GL_FLOAT_MAT4x2:        "GL_FLOAT_MAT4x2",
        GL_FLOAT_MAT4x3:        "GL_FLOAT_MAT4x3",
        GL_SAMPLER_1D:          "GL_SAMPLER_1D",
        GL_SAMPLER_2D:          "GL_SAMPLER_2D",
        GL_SAMPLER_3D:          "GL_SAMPLER_3D",
        GL_SAMPLER_CUBE:        "GL_SAMPLER_CUBE",
        GL_SAMPLER_1D_SHADOW:   "GL_SAMPLER_1D_SHADOW",
        GL_SAMPLER_2D_SHADOW:   "GL_SAMPLER_2D_SHADOW",
        GL_SAMPLER_1D_ARRAY:    "GL_SAMPLER_1D_ARRAY",
        GL_SAMPLER_2D_ARRAY:    "GL_SAMPLER_2D_ARRAY",
        GL_SAMPLER_1D_ARRAY_SHADOW: "GL_SAMPLER_1D_ARRAY_SHADOW",
        GL_SAMPLER_2D_ARRAY_SHADOW: "GL_SAMPLER_2D_ARRAY_SHADOW",
        GL_SAMPLER_2D_MULTISAMPLE:  "GL_SAMPLER_2D_MULTISAMPLE",
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY:    "GL_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_SAMPLER_CUBE_SHADOW: "GL_SAMPLER_CUBE_SHADOW",
        GL_SAMPLER_BUFFER:      "GL_SAMPLER_BUFFER",
        GL_SAMPLER_2D_RECT:     "GL_SAMPLER_2D_RECT",
        GL_SAMPLER_2D_RECT_SHADOW:  "GL_SAMPLER_2D_RECT_SHADOW",
        GL_INT_SAMPLER_1D:      "GL_INT_SAMPLER_1D",
        GL_INT_SAMPLER_2D:      "GL_INT_SAMPLER_2D",
        GL_INT_SAMPLER_3D:      "GL_INT_SAMPLER_3D",
        GL_INT_SAMPLER_CUBE:    "GL_INT_SAMPLER_CUBE",
        GL_INT_SAMPLER_1D_ARRAY:    "GL_INT_SAMPLER_1D_ARRAY",
        GL_INT_SAMPLER_2D_ARRAY:    "GL_INT_SAMPLER_2D_ARRAY",
        GL_INT_SAMPLER_2D_MULTISAMPLE:  "GL_INT_SAMPLER_2D_MULTISAMPLE",
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:    "GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_INT_SAMPLER_BUFFER:  "GL_INT_SAMPLER_BUFFER",
        GL_INT_SAMPLER_2D_RECT: "GL_INT_SAMPLER_2D_RECT",
        GL_UNSIGNED_INT_SAMPLER_1D: "GL_UNSIGNED_INT_SAMPLER_1D",
        GL_UNSIGNED_INT_SAMPLER_2D: "GL_UNSIGNED_INT_SAMPLER_2D",
        GL_UNSIGNED_INT_SAMPLER_3D: "GL_UNSIGNED_INT_SAMPLER_3D",
        GL_UNSIGNED_INT_SAMPLER_CUBE:   "GL_UNSIGNED_INT_SAMPLER_CUBE",
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_1D_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_2D_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE",
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:   "GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
        GL_UNSIGNED_INT_SAMPLER_BUFFER: "GL_UNSIGNED_INT_SAMPLER_BUFFER",
        GL_UNSIGNED_INT_SAMPLER_2D_RECT:    "GL_UNSIGNED_INT_SAMPLER_2D_RECT",
        GL_IMAGE_1D:            "GL_IMAGE_1D",
        GL_IMAGE_2D:            "GL_IMAGE_2D",
        GL_IMAGE_3D:            "GL_IMAGE_3D",
        GL_IMAGE_2D_RECT:       "GL_IMAGE_2D_RECT",
        GL_IMAGE_CUBE:          "GL_IMAGE_CUBE",
        GL_IMAGE_BUFFER:        "GL_IMAGE_BUFFER",
        GL_IMAGE_1D_ARRAY:      "GL_IMAGE_1D_ARRAY",
        GL_IMAGE_2D_ARRAY:      "GL_IMAGE_2D_ARRAY",
        GL_IMAGE_2D_MULTISAMPLE:    "GL_IMAGE_2D_MULTISAMPLE",
        GL_IMAGE_2D_MULTISAMPLE_ARRAY:  "GL_IMAGE_2D_MULTISAMPLE_ARRAY",
        GL_INT_IMAGE_1D:        "GL_INT_IMAGE_1D",
        GL_INT_IMAGE_2D:        "GL_INT_IMAGE_2D",
        GL_INT_IMAGE_3D:        "GL_INT_IMAGE_3D",
        GL_INT_IMAGE_2D_RECT:   "GL_INT_IMAGE_2D_RECT",
        GL_INT_IMAGE_CUBE:      "GL_INT_IMAGE_CUBE",
        GL_INT_IMAGE_BUFFER:    "GL_INT_IMAGE_BUFFER",
        GL_INT_IMAGE_1D_ARRAY:  "GL_INT_IMAGE_1D_ARRAY",
        GL_INT_IMAGE_2D_ARRAY:  "GL_INT_IMAGE_2D_ARRAY",
        GL_INT_IMAGE_2D_MULTISAMPLE:    "GL_INT_IMAGE_2D_MULTISAMPLE",
        GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY:  "GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        GL_UNSIGNED_INT_IMAGE_1D:   "GL_UNSIGNED_INT_IMAGE_1D",
        GL_UNSIGNED_INT_IMAGE_2D:   "GL_UNSIGNED_INT_IMAGE_2D",
        GL_UNSIGNED_INT_IMAGE_3D:   "GL_UNSIGNED_INT_IMAGE_3D",
        GL_UNSIGNED_INT_IMAGE_2D_RECT:  "GL_UNSIGNED_INT_IMAGE_2D_RECT",
        GL_UNSIGNED_INT_IMAGE_CUBE: "GL_UNSIGNED_INT_IMAGE_CUBE",
        GL_UNSIGNED_INT_IMAGE_BUFFER:   "GL_UNSIGNED_INT_IMAGE_BUFFER",
        GL_UNSIGNED_INT_IMAGE_1D_ARRAY: "GL_UNSIGNED_INT_IMAGE_1D_ARRAY",
        GL_UNSIGNED_INT_IMAGE_2D_ARRAY: "GL_UNSIGNED_INT_IMAGE_2D_ARRAY",
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE:   "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE",
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY: "GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY",
        }[ glEnum ]


class Shader( object ):
    """An individual Shader object.

    Used as part of a single ShaderProgram object.

    A vertex shader (GL_VERTEX_SHADER) and a fragment shader (GL_FRAGMENT_SHADER)
    must be used as part of a single Shader Program.
    Geometry shaders (GL_GEOMETRY_SHADER) are optional.

    Shaders can be used by multiple ShaderPrograms.
    """

    @classmethod
    def create_from_existing( cls, type, content, handle ):
        """Creates a Shader object using an existing shader handle
        """
        obj = cls( type, content, False )
        obj._handle = handle
        return obj

    @classmethod
    def create_from_file( cls, type, filename, compile_now = True ):
        with open(filename) as f:
            return cls( type, f.readlines(), compile_now )

    def __init__( self, type, content, compile_now = True ):
        super( Shader, self ).__init__()

        self.type = type
        self.content = content
        self._handle = None

        if compile_now:
            self.compile()

    @property
    def handle( self ):
        return self._handle

    def compile( self ):
        """Compiles the shader using the current content
        value.

        This is required before a ShaderProgram is linked.

        This is not required to be performed in order to
        attach a Shader to a ShaderProgram. As long as the
        Shader is compiled prior to the ShaderProgram being
        linked.
        """
        self._handle = glCreateShader( self.type )

        glShaderSource( self.handle, self.content )

        # compile the shader
        glCompileShader( self.handle )

        # retrieve the compile status
        if not glGetShaderiv( self.handle, GL_COMPILE_STATUS ):
            self._print_shader_errors( glGetShaderInfoLog( self.handle ) )
            return False

        return True

    def _print_shader_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        # print the log to the console
        errors = parse_shader_errors( buffer )
        lines = self.content.split('\n')

        for error in errors:
            line, desc = error

            print "Error compiling shader type: %s" % enum_to_string( self.type )
            print "\tLine: %i" % line
            print "\tDescription: %s" % desc
            print "\tCode: %s" % lines[ line - 1 ]


class ShaderProgram( object ):
    """Defines a complete Shader Program, consisting of at least
    a vertex and fragment shader.
    
    Shader objects are decoupled from ShaderPrograms to avoid recompilation
    when re-using shaders.

    Multiple shaders of the same type can be attached together.
    This lets you combine multiple smaller shaders into a single larger one.

    kwargs supported arguments:
        raise_invalid_variables:    defaults to False. If set to True,
            accessing invalid Uniforms and Attributes will trigger a
            ValueError exception to be raised.
    """
    
    def __init__( self, link_now = True, *args, **kwargs ):
        # create the program handle
        self._handle = glCreateProgram()

        # store our attribute and uniform handler
        self.attributes = Attributes( self )
        self.uniforms = Uniforms( self )

        for shader in args:
            self.attach_shader( shader )

        self.raise_invalid_variables = \
            False if 'raise_invalid_variables' not in kwargs \
            else kwargs['raise_invalid_variables']

        if link_now:
            self.link()

    @property
    def handle( self ):
        return self._handle

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
            print "Error attaching shader type: %s" % enum_to_string( shader.type )
            print "\tException: %s" % str(e)

            # chain the exception
            raise

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

    def link( self ):
        """Links the specified shader into a complete program.

        It is important to set any attribute locations and
        the frag data location BEFORE calling link or these calls
        will not take effect.
        """
        # link the program
        glLinkProgram( self.handle )

        # retrieve the compile status
        if not glGetProgramiv( self.handle, GL_LINK_STATUS ):
            self._print_shader_errors( glGetProgramInfoLog( self.handle ) )
            return False

        self.uniforms._on_program_linked()
        self.attributes._on_program_linked()
        return True

    def _print_shader_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        print "Error linking shader:"
        print "\tDescription: %s" % ( buffer )

        # print the log to the console
        errors = parse_shader_errors( buffer )

        for error in errors:
            line, desc = error

            print "Error linking shader"
            print "\tDescription: %s" % ( desc )

    @property
    def linked( self ):
        """Returns the link status of the shader.
        """
        return glGetProgramiv( self.handle, GL_LINK_STATUS ) == GL_TRUE

    def bind( self ):
        """Binds the shader program to be the active shader program.

        The shader MUST be linked for this to be valid.

        It is valid to bind one shader after another without calling
        unbind.
        """
        # bind the program
        glUseProgram( self.handle )

    def unbind( self ):
        """Unbinds the shader program.

        This sets the current shader to null.

        It is valid to bind one shader after another without calling
        unbind.
        Be aware that this will NOT unwind the bind calls.
        Calling unbind will set the active shader to null.
        """
        # unbind the
        glUseProgram( 0 )

    @property
    def bound( self ):
        """Returns True if the program is the currently bound program
        """
        return glGetIntegerv( GL_CURRENT_PROGRAM ) == self.handle


class Uniforms( object ):
    """Provides access to ShaderProgram uniform variables.

    Usage:
    shader.attributes.in_position = 0
    print shader.attributes.in_position

    shader.attributes[ 'in_position' ] = 0
    print shader.attributes[ 'in_position' ]
    """

    """This dictionary holds a list of GL shader enum types.
    Each type has a corresponding Uniform class.
    When processing uniforms, the appropriate class is instantiated
    for the specific time.

    The values are populated later.
    """
    types = {}

    def __init__( self, program ):
        super( Uniforms, self ).__init__()

        self.__dict__[ 'program' ] = program

    def _on_program_linked( self ):
        """Called by a ShaderProgram when the program is linked
        successfully.
        """
        # clear the existing uniforms, if any
        for key, value in self.__dict__.items():
            if key != 'program':
                del self.__dict__[ key ]

        # iterate through our auto-detected uniforms
        # and create objects for them
        for name, type in self._gl_all():
            # instantiate the uniform object for the specified type
            self.__dict__[ name ] = self.types[ type ]()
            self.__dict__[ name ]._set_data( name, self.program )

    def _gl_all( self ):
        """Returns a list of all the available uniforms.

        The list is composed of tuples. Each tuple is
        composed of the name and the GLtype (as a string)
        of the uniform.
        """
        # get number of active uniforms
        handle = self.__dict__[ 'program' ].handle
        return [
            (name, type) for name, size, type in uniforms( handle )
            ]

    def all( self ):
        """Returns a dictionary of all uniform objects.

        The key is the uniform name.
        The value is the uniform type as a string.
        Any uniform automatically detected or accessed programmatically
        in python will appear in this list.
        """
        _uniforms = self.__dict__.copy()
        del _uniforms['program']
        # convert to a list
        return _uniforms

    def __getattr__( self, name ):
        """Simply calls __getitem__ with the same parameters.
        """
        return self.__getitem__( name )

    def __getitem__( self, name ):
        """Returns an appropriate uniform for the specified variable name.

        This variable name matches the uniform specified in the shader.

        The ShaderProgram MUST be linked or a ValueError is raised.
        """
        if not self.__dict__[ 'program' ].linked:
            raise ValueError( "ShaderProgram must be linked before attribute can be queried" )

        # check if a uniform already exists
        if name in self.__dict__:
            # return the existing uniform
            return self.__dict__[ name ]
        else:
            if self.__dict__[ 'program' ].raise_invalid_variables:
                raise ValueError( "Uniform '%s' not specified in ShaderProgram" % name )
            else:
                self.__dict__[ name ] = InvalidUniform()
                self.__dict__[ name ]._set_data( name, self.program )
                return self.__dict__[ name ]

    def __setattr__( self, name, value ):
        self.__setitem__( name, value )

    def __setitem__( self, name, value ):
        """Passes the value to the uniform's value member.

        This lets us just call 'Uniforms.variable = value'
        """
        if isinstance( value, Uniform ):
            # allow the manual assignment of uniforms
            if name in self.__dict__:
                raise ValueError( "Uniform already set '%s'" % name )
            self.__dict__[ name ] = value
            value._set_data( name, self.program )
        else:
            self.__getitem__( name ).value = value


class Uniform( object ):
    """Provides the base class for access to uniform variables.
    """

    def __init__( self ):
        super( Uniform, self ).__init__()

        # name and program is set when this uniform is assigned to
        # a member of the Uniforms class
        # location is the updated
        self.name = None
        self.program = None
        self._location = None

    @property
    def gl_type( self ):
        """Extracts the values for the uniform.
        """
        # result may be None type
        _uniform = uniform( self.program.handle, self.name )
        if _uniform:
            return _uniform[ 2 ]
        return None

    @property
    def type( self ):
        """Extracts the values for the uniform.
        """
        # result may be None type
        return enum_to_string( self.gl_type )

    def _set_data( self, name, program ):
        """Used by the Uniforms class to pass the uniform name
        and ShaderProgram.
        """
        self.name = name
        self.program = program

        if not self.program.linked:
            raise ValueError( "ShaderProgram must be linked before uniform can be set" )

        # set our location
        self._location = glGetUniformLocation( self.program.handle, self.name )

    @property
    def location( self ):
        return self._location

    @property
    def value( self ):
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        raise NotImplementedError


class InvalidUniform( Uniform ):

    def __init__( self ):
        super( InvalidUniform, self ).__init__()

    def _set_data( self, name, program ):
        Uniform._set_data( self, name, program )

        # ensure we have the right uniform type
        print "Uniform '%s' not specified in ShaderProgram" % name

    @property
    def value( self ):
        pass

    @value.setter
    def value( self, *args ):
        pass


class UniformFloat( Uniform ):
    types = [
        GL_FLOAT,
        GL_FLOAT_VEC2,
        GL_FLOAT_VEC3,
        GL_FLOAT_VEC4
        ]

    def __init__( self ):
        super( UniformFloat, self ).__init__()

    def _set_data( self, name, program ):
        super( UniformFloat, self )._set_data( name, program )

        # ensure we have the right uniform type
        if self.gl_type not in self.types:
            raise ValueError( "Uniform '%s' is not of type Float" % self.name )

    @property
    def value( self ):
        """Returns the values stored in the uniform.

        Not yet implemented.
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Sets the float values for the uniform.

        The OpenGL function is chosen based on the number of dimensions
        of arguments.
        If a single dimension is provided (values are passed individually),
        the values are passed using the glUniform[1,2,3,4]f functions.

        If more than 1 dimension is present, then the final dimension
        is used to select the OpenGL function to use.

        The number of values is calculated as the total number
        of values divided by uniform function size.

        It is acceptable to set uniforms individually.
        For example:
        value = 1.0, 2.0, 3.0
        This will use glUniform3f.

        Passing a list of values will use the array functionality.
        For example:
        value = [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ],
                [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ]
        This will use the glUniform2fv function.
        The count will be 6 (12 / 2).

        It is acceptable to set uniforms as a single list.
        For example:
        value = [
            [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ],
            [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ]
            ]
        This will use the glUniform2fv function.
        The count will be 6 (12 / 2).
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = 'float32' )

        func, size = {
            GL_FLOAT:             (glUniform1fv, 1),
            GL_FLOAT_VEC2:        (glUniform2fv, 2),
            GL_FLOAT_VEC3:        (glUniform3fv, 3),
            GL_FLOAT_VEC4:        (glUniform4fv, 4),
            }[ self.gl_type ]

        count = values.size / size
        func( self.location, count, values )


class UniformInt( Uniform ):
    types = [
        GL_INT,
        GL_INT_VEC2,
        GL_INT_VEC3,
        GL_INT_VEC4
        ]

    def __init__( self ):
        super( UniformInt, self ).__init__()

    def _set_data( self, name, program ):
        super( UniformInt, self )._set_data( name, program )

        # ensure we have the right uniform type
        if self.gl_type not in self.types:
            raise ValueError( "Uniform '%s' is not of type Int" % self.name )

    @property
    def value( self ):
        """Returns the values stored in the uniform.

        Not yet implemented.
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Sets the integer values for the uniform.

        The OpenGL function is chosen based on the number of dimensions
        of arguments.
        If a single dimension is provided (values are passed individually),
        the values are passed using the glUniform[1,2,3,4]i functions.

        If more than 1 dimension is present, then the final dimension
        is used to select the OpenGL function to use.

        The number of values is calculated as the total number
        of values divided by uniform function size.

        It is acceptable to set uniforms individually.
        For example:
        value = 1, 2, 3
        This will use glUniform3i.

        Passing a list of values will use the array functionality.
        For example:
        value = [ 255, -255 ], [ -255, 255 ], [ -255, 0 ],
                [ 255, -255 ], [ -255, 255 ], [ -255, 0 ]
        This will use the glUniform2iv function.
        The count will be 6 (12 / 2).

        It is acceptable to set uniforms as a single list.
        For example:
        value = [
            [ 255, -255 ], [ -255, 255 ], [ -255, 0 ],
            [ 255, -255 ], [ -255, 255 ], [ -255, 0 ]
            ]
        This will use the glUniform2iv function.
        The count will be 6 (12 / 2).
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = 'int32' )

        func, size = {
            GL_INT:             (glUniform1iv, 1),
            GL_INT_VEC2:        (glUniform2iv, 2),
            GL_INT_VEC3:        (glUniform3iv, 3),
            GL_INT_VEC4:        (glUniform4iv, 4),
            }[ self.gl_type ]

        count = values.size / size
        func( self.location, count, values )


class UniformUint( Uniform ):
    types =[
        GL_UNSIGNED_INT,
        GL_UNSIGNED_INT_VEC2,
        GL_UNSIGNED_INT_VEC3,
        GL_UNSIGNED_INT_VEC4,
        GL_UNSIGNED_INT_ATOMIC_COUNTER,
        ]

    def __init__( self ):
        super( UniformUint, self ).__init__()

    def _set_data( self, name, program ):
        super( UniformUint, self )._set_data( name, program )

        # ensure we have the right uniform type
        if self.gl_type not in self.types:
            raise ValueError( "Uniform '%s' is not of type Uint" % self.name )

    @property
    def value( self ):
        """Returns the values stored in the uniform.

        Not yet implemented.
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Sets the unsigned integer values for the uniform.

        The OpenGL function is chosen based on the number of dimensions
        of arguments.
        If a single dimension is provided (values are passed individually),
        the values are passed using the glUniform[1,2,3,4]ui functions.

        If more than 1 dimension is present, then the final dimension
        is used to select the OpenGL function to use.

        The number of values is calculated as the total number
        of values divided by uniform function size.

        It is acceptable to set uniforms individually.
        For example:
        value = 1, 2, 3
        This will use glUniform3ui.

        Passing a list of values will use the array functionality.
        For example:
        value = [ 255, 0 ], [ 0, 255 ], [ 0, 0 ],
                [ 255, 0 ], [ 0, 255 ], [ 0, 0 ]
        This will use the glUniform2uiv function.
        The count will be 6 (12 / 2).

        It is acceptable to set uniforms as a single list.
        For example:
        value = [
            [ 255, 0 ], [ 0, 255 ], [ 0, 0 ],
            [ 255, 0 ], [ 0, 255 ], [ 0, 0 ]
            ]
        This will use the glUniform2uiv function.
        The count will be 6 (12 / 2).
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = 'uint32' )

        func, size = {
            GL_UNSIGNED_INT:                (glUniform1uiv, 1),
            GL_UNSIGNED_INT_VEC2:           (glUniform2uiv, 2),
            GL_UNSIGNED_INT_VEC3:           (glUniform3uiv, 3),
            GL_UNSIGNED_INT_VEC4:           (glUniform4uiv, 4),
            GL_UNSIGNED_INT_ATOMIC_COUNTER: (glUniform1uiv, 1),
            }[ self.gl_type ]

        count = values.size / size
        func( self.location, count, values )


class UniformFloatMatrix( Uniform ):
    types = [
        GL_FLOAT_MAT2,
        GL_FLOAT_MAT3,
        GL_FLOAT_MAT4,
        GL_FLOAT_MAT2x3,
        GL_FLOAT_MAT2x4,
        GL_FLOAT_MAT3x2,
        GL_FLOAT_MAT3x4,
        GL_FLOAT_MAT4x2,
        GL_FLOAT_MAT4x3
        ]

    def __init__( self ):
        super( UniformFloatMatrix, self ).__init__()

    def _set_data( self, name, program ):
        super( UniformFloatMatrix, self )._set_data( name, program )

        # ensure we have the right uniform type
        if self.gl_type not in self.types:
            raise ValueError( "Uniform '%s' is not of type Uint" % self.name )

    @property
    def value( self ):
        """Returns the values stored in the uniform.

        Not yet implemented.
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Sets the matrix values for the uniform.

        The OpenGL function is chosen based on the last 2 dimensions
        of the arguments.
        The second last dimension is the number of rows.
        The last dimension is the number of columns.
        The matrix count is determined by using the total number of values
        divided by the size of each matrix.

        For example:
        value = [ [1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ] ]
        The matrix size is 2x3 and will use the function glUniformMatrix3x2fv.
        The count will be 1.

        It is acceptable to set matrices individually.
        For example:
        value = [ [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ] ],
                [ [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ] ]
        This will use the glUniformMatrix3x2fv function.
        The count will be 2 (12 / 6).

        It is acceptable to set matrices as a single list.
        For example:
        value = [
            [ [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ] ],
            [ [ 1.0, 0.0 ], [ 0.0, 1.0 ], [ 0.0, 0.0 ] ]
            ]
        This will use the glUniformMatrix3x2fv function.
        The count will be 2 (12 / 6).
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = 'float32' )

        func, size = {
            GL_FLOAT_MAT2:      (glUniformMatrix2fv,    4),
            GL_FLOAT_MAT3:      (glUniformMatrix3fv,    9),
            GL_FLOAT_MAT4:      (glUniformMatrix4fv,    16),
            GL_FLOAT_MAT2x3:    (glUniformMatrix2x3fv,  6),
            GL_FLOAT_MAT2x4:    (glUniformMatrix2x4fv,  8),
            GL_FLOAT_MAT3x2:    (glUniformMatrix3x2fv,  6),
            GL_FLOAT_MAT3x4:    (glUniformMatrix3x4fv,  12),
            GL_FLOAT_MAT4x2:    (glUniformMatrix4x2fv,  8),
            GL_FLOAT_MAT4x3:    (glUniformMatrix4x3fv,  12),
            }[ self.gl_type ]

        count = values.size / size
        func( self.location, count, False, values )


class UniformSampler( UniformInt ):
    types = [
        GL_SAMPLER_1D,
        GL_SAMPLER_2D,
        GL_SAMPLER_3D,
        GL_SAMPLER_CUBE,
        GL_SAMPLER_1D_SHADOW,
        GL_SAMPLER_2D_SHADOW,
        GL_SAMPLER_1D_ARRAY,
        GL_SAMPLER_2D_ARRAY,
        GL_SAMPLER_1D_ARRAY_SHADOW,
        GL_SAMPLER_2D_ARRAY_SHADOW,
        GL_SAMPLER_2D_MULTISAMPLE,
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY,
        GL_SAMPLER_CUBE_SHADOW,
        GL_SAMPLER_BUFFER,
        GL_SAMPLER_2D_RECT,
        GL_SAMPLER_2D_RECT_SHADOW,
        GL_INT_SAMPLER_1D,
        GL_INT_SAMPLER_2D,
        GL_INT_SAMPLER_3D,
        GL_INT_SAMPLER_CUBE,
        GL_INT_SAMPLER_1D_ARRAY,
        GL_INT_SAMPLER_2D_ARRAY,
        GL_INT_SAMPLER_2D_MULTISAMPLE,
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY,
        GL_INT_SAMPLER_BUFFER,
        GL_INT_SAMPLER_2D_RECT,
        GL_UNSIGNED_INT_SAMPLER_1D,
        GL_UNSIGNED_INT_SAMPLER_2D,
        GL_UNSIGNED_INT_SAMPLER_3D,
        GL_UNSIGNED_INT_SAMPLER_CUBE,
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_BUFFER,
        GL_UNSIGNED_INT_SAMPLER_2D_RECT,
        GL_IMAGE_1D,
        GL_IMAGE_2D,
        GL_IMAGE_3D,
        GL_IMAGE_2D_RECT,
        GL_IMAGE_CUBE,
        GL_IMAGE_BUFFER,
        GL_IMAGE_1D_ARRAY,
        GL_IMAGE_2D_ARRAY,
        GL_IMAGE_2D_MULTISAMPLE,
        GL_IMAGE_2D_MULTISAMPLE_ARRAY,
        GL_INT_IMAGE_1D,
        GL_INT_IMAGE_2D,
        GL_INT_IMAGE_3D,
        GL_INT_IMAGE_2D_RECT,
        GL_INT_IMAGE_CUBE,
        GL_INT_IMAGE_BUFFER,
        GL_INT_IMAGE_1D_ARRAY,
        GL_INT_IMAGE_2D_ARRAY,
        GL_INT_IMAGE_2D_MULTISAMPLE,
        GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY,
        GL_UNSIGNED_INT_IMAGE_1D,
        GL_UNSIGNED_INT_IMAGE_2D,
        GL_UNSIGNED_INT_IMAGE_3D,
        GL_UNSIGNED_INT_IMAGE_2D_RECT,
        GL_UNSIGNED_INT_IMAGE_CUBE,
        GL_UNSIGNED_INT_IMAGE_BUFFER,
        GL_UNSIGNED_INT_IMAGE_1D_ARRAY,
        GL_UNSIGNED_INT_IMAGE_2D_ARRAY,
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE,
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY,
        ]

    def __init__( self ):
        super( UniformSampler, self ).__init__()

    def _set_data( self, name, program ):
        Uniform._set_data( self, name, program )

        # ensure we have the right uniform type
        if self.gl_type not in self.types:
            raise ValueError( "Uniform '%s' is not of type Sampler" % self.name )


class Attributes( object ):
    """Provides access to ShaderProgram attribute bindings.

    Because Attributes must be updated before the shader is linked,
    we cannot do the same validation as we can with Uniforms.

    Usage:
    shader.attributes.in_position = 0
    print shader.attributes.in_position

    shader.attributes[ 'in_position' ] = 0
    print shader.attributes[ 'in_position' ]
    """

    def __init__( self, program ):
        super( Attributes, self ).__init__()

        self.__dict__[ 'program' ] = program

    def _on_program_linked( self ):
        pass

    def all( self ):
        """Returns a dictionary of all the available attributes.

        The key is the attribute name.
        The value is the attribute type as a string.
        """
        # get number of active attributes
        handle = self.__dict__[ 'program' ].handle
        num_attributes = glGetProgramiv( handle, GL_ACTIVE_ATTRIBUTES )

        attributes = {}

        for index in range( num_attributes ):
            name_length = 30
            glNameSize = (GLsizei)()
            glSize = (GLint)()
            glType = (GLenum)()
            glName = (GLchar * name_length)()

            glGetActiveAttrib(
                handle,
                index,
                name_length,
                glNameSize,
                glSize,
                glType,
                glName
                )

            attributes[ glName.value ] = enum_to_string( glType.value )
        return attributes

    def __getattr__( self, name ):
        """Simply calls __getitem__ with the same parameters.
        """
        return self.__getitem__( name )

    def __getitem__( self, name ):
        """Returns the currently bound attribute value.

        The ShaderProgram MUST be linked or a ValueError is raised.

        If the attribute is invalid, None will be returned.
        An invalid attribute is signified as OpenGL's glGetAttribLocation
        function returning -1.
        """
        if not self.program.linked:
            raise ValueError( "ShaderProgram must be linked before attribute can be queried" )

        location = glGetAttribLocation( self.program.handle, name )

        # return None if the location is invalid
        if location < 0:
            return None
        return location

    def __setattr__( self, name, value ):
        """Simply calls __setitem__ with the same parameters
        """
        return self.__setitem__( name, value )

    def __setitem__( self, name, value ):
        """Sets the shader's attribute for the specified name.

        This value can be set at any time on the ShaderProgram, but it
        will only take effect the next time the ShaderProgram is linked.
        """
        glBindAttribLocation( self.program.handle, value, name )


# register our uniform types
def register_uniforms():
    """Registers our uniform class types with the central
    Uniforms class.

    This is called automatically on import and does not need
    to be called manually.
    Calling this multiple times will not do any harm.
    """
    for type in UniformFloat.types:
        Uniforms.types[ type ] = UniformFloat
    for type in UniformInt.types:
        Uniforms.types[ type ] = UniformInt
    for type in UniformUint.types:
        Uniforms.types[ type ] = UniformUint
    for type in UniformFloatMatrix.types:
        Uniforms.types[ type ] = UniformFloatMatrix
    for type in UniformSampler.types:
        Uniforms.types[ type ] = UniformSampler
register_uniforms()

