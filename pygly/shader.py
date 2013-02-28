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
        name is the variable name
        size is the variable size in bytes
        type is the GL enumeration
    """
    # get number of active uniforms
    num_uniforms = glGetProgramiv( handle, GL_ACTIVE_UNIFORMS )

    for index in range( num_uniforms ):
        yield uniform_for_index( handle, index )

def uniform_for_index( handle, index ):
    name, size, type = glGetActiveUniform( handle, index )
    return name, size, type

def uniform_for_name( handle, name ):
    # we can't get uniforms directly
    # we have to iterate over the active uniforms and find our
    # uniform match by the name given
    for uniform in uniforms( handle ):
        _name, _size, _type = uniform

        if _name == name:
            return _name, _size, _type

    # no match found
    return None

def attributes( handle ):
    """Returns an iterator for the attributes of the specified program.

    Each attribute returns a tuple with the following values:
        name, size, type
    Where:
        name is the variable name
        size is the variable size in bytes
        type is the GL enumeration
    """
    # get number of active uniforms
    num_attributes = glGetProgramiv( handle, GL_ACTIVE_ATTRIBUTES )

    for index in range( num_attributes ):
        yield attribute_for_index( handle, index )

def attribute_for_index( handle, index ):
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

    name, size, type = glName.value, glSize.value, glType.value
    return name, size, type

def attribute_for_name( handle, name ):
    # we can't get attributes directly
    # we have to iterate over the active attributes and find our
    # attribute match by the name given
    for attribute in attributes( handle ):
        _name, _size, _type = attribute

        if _name == name:
            return _name, _size, _type

    # no match found
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
    def create_from_existing( cls, type, source, handle ):
        """Creates a Shader object using an existing shader handle
        """
        obj = cls( type, source, False )
        obj._handle = handle
        return obj

    @classmethod
    def create_from_file( cls, type, filename, compile_now = True ):
        with open(filename) as f:
            return cls( type, f.readlines(), compile_now )

    def __init__( self, type, source, compile_now = True ):
        super( Shader, self ).__init__()

        self._handle = None
        self._type = type
        self._source = source

        if compile_now:
            self.compile()

    @property
    def handle( self ):
        return self._handle

    @property
    def type( self ):
        return self._type

    @property
    def source( self ):
        return self._source

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

        glShaderSource( self.handle, self.source )

        # compile the shader
        glCompileShader( self.handle )

        # retrieve the compile status
        if not glGetShaderiv( self.handle, GL_COMPILE_STATUS ):
            errors = glGetShaderInfoLog( self.handle )
            self._print_shader_errors( errors )
            return False

        return True

    def _print_shader_errors( self, buffer ):
        """Parses the error buffer and prints it to the console.

        The buffer should be the exact contents of the GLSL
        error buffer converted to a Python String.
        """
        # print the log to the console
        errors = parse_shader_errors( buffer )
        lines = self.source.split('\n')

        for error in errors:
            line, desc = error

            print "Error compiling shader type: %s" % enum_to_string( self.type )
            print "\tLine: %i" % line
            print "\tDescription: %s" % desc
            print "\tCode: %s" % lines[ line - 1 ]

    def __str__( self ):
        string = "Shader:\t%s" % ( enum_to_string( self.type ) )
        return string


class ShaderProgram( object ):
    """Defines a complete Shader Program, consisting of at least
    a vertex and fragment shader.
    
    Shader objects are decoupled from ShaderPrograms to avoid recompilation
    when re-using shaders.

    Multiple shaders of the same type can be attached together.
    This lets you combine multiple smaller shaders into a single larger one.

    kwargs supported arguments:
        link_now: defaults to True. If set to True, the shader will be linked
            during the constructor.
        raise_invalid_variables:    defaults to False. If set to True,
            accessing invalid Uniforms and Attributes will trigger a
            ValueError exception to be raised.
    """
    
    def __init__( self, *args, **kwargs ):
        # create the program handle
        self._handle = glCreateProgram()

        # store our attribute and uniform handler
        self.attributes = Attributes( self )
        self.uniforms = Uniforms( self )

        for shader in args:
            self.attach_shader( shader )

        # default raise exception to False
        self.raise_invalid_variables = kwargs.get(
                'raise_invalid_variables',
                False
                )

        # default link now to True
        link_now = kwargs.get( 'link_now', True )

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
            errors = glGetProgramInfoLog( self.handle )
            self._print_shader_errors( errors )
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

    def __str__( self ):
        string = \
            "ShaderProgram:\n" \
            "Linked:\t%s\n" \
            "%s\n" \
            "%s" % (
            str(self.linked),
            str(self.attributes),
            str(self.uniforms)
            )
        return string


class Uniforms( object ):
    """Provides access to ShaderProgram uniform variables.

    Uniforms can be accessed as members:
    shader.uniforms.model_view = 0
    print shader.uniforms.model_view
    >>> 0

    Uniforms can also be accessed array style:
    shader.uniforms[ 'model_view' ] = 0
    print shader.uniforms[ 'model_view' ]
    >>> 0

    Uniforms provides a mechanism to iterate over the active Uniforms:
    for uniform in shader.uniforms:
        print uniform
    """

    """This dictionary holds a list of GL shader enum types.
    Each type has a corresponding Uniform class.
    When processing uniforms, the appropriate class is instantiated
    for the specific time.

    The values are populated by calling 'register_uniform_class'.
    """
    types = {}

    @staticmethod
    def register_uniform_class( class_type, types ):
        """Registers a Uniform class to be used for specific GLSL GL types.

        class_type is a class type, such as UniformFloat.
        types is a list of GL enumeration types that the class is to be used for.
        Such as GL_FLOAT_VEC4, GL_SAMPLER_1D, etc.

        There is no checking for duplicates, latter calls to this function can over-ride
        existing class registrations.
        """
        for type in types:
            Uniforms.types[ type ] = class_type

    def __init__( self, program ):
        super( Uniforms, self ).__init__()

        self.__dict__[ 'program' ] = program

    def __iter__( self ):
        return self.next()

    def next( self ):
        for uniform in self.all().values():
            yield uniform

    def _on_program_linked( self ):
        """Called by a ShaderProgram when the program is linked
        successfully.
        """
        # clear the existing uniforms, if any
        for key, value in self.__dict__.items():
            if key != 'program':
                del self.__dict__[ key ]

        # get our active uniforms
        program = self.__dict__[ 'program' ]
        for name, size, type in uniforms( program.handle ):
            self.__dict__[ name ] = self.types[ type ]()
            self.__dict__[ name ]._set_data( program, name, type )

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
            # the uniform doesn't exit
            # check if we should raise an exception
            # if not, create an InvalidUniform object and store it
            # this means it will only print a log message this one time
            if self.__dict__[ 'program' ].raise_invalid_variables:
                raise ValueError( "Uniform '%s' not specified in ShaderProgram" % name )
            else:
                # we shouldn't raise an exception
                # so create an invalid uniform object that will do nothing
                program = self.__dict__[ 'program' ]
                self.__dict__[ name ] = InvalidUniform()
                self.__dict__[ name ]._set_data( program, name, type = None )
                return self.__dict__[ name ]

    def __setattr__( self, name, value ):
        self.__setitem__( name, value )

    def __setitem__( self, name, value ):
        """Passes the value to the uniform's value member.

        This lets us just call 'Uniforms.variable = value'
        """
        if isinstance( value, Uniform ):
            # the value is an instance of Uniform
            # so it must be to do an assignment of the object itself
            if name in self.__dict__:
                raise ValueError( "Replacing Uniform: %s" % name )
            self.__dict__[ name ] = value
            value._set_data( name, self.program )
        else:
            # the value isn't a Uniform class
            # so pass it to the existing uniform
            self.__getitem__( name ).value = value

    def __str__( self ):
        string = "Uniforms:\n"
        for uniform in self:
            string += str(uniform) + "\n"
        return string[:-1]


class Uniform( object ):
    """Provides the base class for access to uniform variables.
    """

    def __init__( self, types, dtype ):
        """Creates a new Uniform object.

        This should only be called by inherited Uniform classes.

        Types is a dictionary with the following format:
        key: GL enumeration type, Eg. GL_FLOAT_VEC4.
        value: (uniform setter function, number of values per variable)

        The function is used when setting the uniform value.

        The number of values per variable is used to determine the number of
        variables passed to a uniform.
        Ie. Numver of variables = number of values / values per variable
        """
        super( Uniform, self ).__init__()

        self._types = types
        self._dtype = dtype

        # these values are set in _set_data which is called by
        # shader.uniforms when an assignment is made
        # this allows users to create uniforms and assign them to
        # a shader
        self._program = None
        self._name = None
        self._type = None
        self._func = None
        self._num_values = None
        self._location = None

    @property
    def name( self ):
        """Returns the name of the uniform as specified in GLSL.

        Eg. in_texture_diffuse
        """
        return self._name

    @property
    def program( self ):
        """Returns the ShaderProgram that owns the Uniform.
        """
        return self._program

    @property
    def location( self ):
        """Returns the location of the Uniform.
        """
        return self._location

    @property
    def type( self ):
        """Returns the GL enumeration type for the Uniform.

        Eg. GL_FLOAT_VEC4.
        """
        return self._type

    def _set_data( self, program, name, type ):
        """Used by the 'Uniforms' class to pass the data to the Uniform
        object once it is assigned to a ShaderProgram.
        """
        self._program = program
        self._name = name
        self._type = type

        if not self.program.linked:
            raise ValueError( "ShaderProgram must be linked before uniform can be set" )

        # ensure we have the right uniform type
        if self.type not in self._types:
            raise ValueError(
                "Uniform '%s' has type '%s' and is not supporte by " % (
                    self.name,
                    enum_to_string( self.type ),
                    self.__class__.__name__
                    )
                )

        self._func, self._num_values = self._types[ self.type ]

        # set our location
        self._location = glGetUniformLocation( self.program.handle, self.name )

    @property
    def value( self ):
        """Retrieves the current value of the Uniform.
        """
        raise NotImplementedError

    @value.setter
    def value( self, *args ):
        """Assigns a value to the Uniform.
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = self._dtype )
        count = values.size / self._num_values
        self._func( self.location, count, values )

    def __str__( self ):
        """Returns a human readable string representing the Uniform.
        """
        return "%s:\t%s\t%s\t%d" % (
            self.__class__.__name__,
            self.name,
            enum_to_string( self.type ),
            self.location
            )

class InvalidUniform( Uniform ):
    """Represents an InvalidUniform.

    These are used when exceptions are disabled for invalid uniforms
    and the user attempts to access a uniform that doesn't exist or
    isn't in use.

    If a variable is declared in a GLSL shader but not used in any
    of the code, GLSL will consider it to not exist.
    """

    def __init__( self ):
        super( InvalidUniform, self ).__init__(
            {},
            None
            )

    def _set_data( self, program, name, type ):
        # ensure we have the right uniform type
        print "Uniform '%s' not specified in ShaderProgram" % name

    @property
    def value( self ):
        """Always returns None
        """
        return None

    @value.setter
    def value( self, *args ):
        """Stub function that does nothing.
        """
        pass


class UniformFloat( Uniform ):
    """Wraps GLSL Float Uniform types.
    """

    types = {
        GL_FLOAT:       (glUniform1fv,  1),
        GL_FLOAT_VEC2:  (glUniform2fv,  2),
        GL_FLOAT_VEC3:  (glUniform3fv,  3),
        GL_FLOAT_VEC4:  (glUniform4fv,  4),
        }

    def __init__( self ):
        super( UniformFloat, self ).__init__(
            UniformFloat.types,
            'float32'
            )


class UniformInt( Uniform ):
    """Wraps GLSL Int Uniform types.
    """

    types = {
        GL_INT:         (glUniform1iv,  1),
        GL_INT_VEC2:    (glUniform2iv,  2),
        GL_INT_VEC3:    (glUniform3iv,  3),
        GL_INT_VEC4:    (glUniform4iv,  4),
        }

    def __init__( self ):
        super( UniformInt, self ).__init__(
            UniformInt.types,
            'int32'
            )


class UniformUint( Uniform ):
    """Wraps GLSL Unsigned Int Uniform types.
    """

    types = {
        GL_UNSIGNED_INT:        (glUniform1uiv,     1),
        GL_UNSIGNED_INT_VEC2:   (glUniform2uiv,     2),
        GL_UNSIGNED_INT_VEC3:   (glUniform3uiv,     3),
        GL_UNSIGNED_INT_VEC4:   (glUniform4uiv,     4),
        GL_UNSIGNED_INT_ATOMIC_COUNTER: (glUniform1uiv, 1),
        }

    def __init__( self ):
        super( UniformUint, self ).__init__(
            UniformUint.types,
            'uint32'
            )


class UniformFloatMatrix( Uniform ):
    """Wraps GLSL Float Matrix Uniform types.
    """

    types = {
        GL_FLOAT_MAT2:      (glUniformMatrix2fv,    4),
        GL_FLOAT_MAT3:      (glUniformMatrix3fv,    9),
        GL_FLOAT_MAT4:      (glUniformMatrix4fv,    16),
        GL_FLOAT_MAT2x3:    (glUniformMatrix2x3fv,  6),
        GL_FLOAT_MAT2x4:    (glUniformMatrix2x4fv,  8),
        GL_FLOAT_MAT3x2:    (glUniformMatrix3x2fv,  6),
        GL_FLOAT_MAT3x4:    (glUniformMatrix3x4fv,  12),
        GL_FLOAT_MAT4x2:    (glUniformMatrix4x2fv,  8),
        GL_FLOAT_MAT4x3:    (glUniformMatrix4x3fv,  12),
        }

    def __init__( self ):
        super( UniformFloatMatrix, self ).__init__(
            UniformFloatMatrix.types,
            'float32'
            )

    @Uniform.value.setter
    def value( self, *args ):
        """Sets the matrix values for the uniform.

        This over-ride is required as the matrix methods have an extra
        parameter for transposing a matrix.
        """
        if not self.program.bound:
            raise ValueError( "ShaderProgram must be bound before uniform can be set" )

        values = numpy.array( args, dtype = self._dtype )
        count = values.size / self._num_values
        self._func( self.location, count, False, values )


class UniformSampler( Uniform ):
    """Wraps GLSL Sampler Uniform types.

    These are the same as UniformInt, but are seperated for convenience.
    """

    types = {
        GL_SAMPLER_1D:          (glUniform1iv,  1),
        GL_SAMPLER_2D:          (glUniform1iv,  1),
        GL_SAMPLER_3D:          (glUniform1iv,  1),
        GL_SAMPLER_CUBE:        (glUniform1iv,  1),
        GL_SAMPLER_1D_SHADOW:   (glUniform1iv,  1),
        GL_SAMPLER_2D_SHADOW:   (glUniform1iv,  1),
        GL_SAMPLER_1D_ARRAY:    (glUniform1iv,  1),
        GL_SAMPLER_2D_ARRAY:    (glUniform1iv,  1),
        GL_SAMPLER_1D_ARRAY_SHADOW: (glUniform1iv,  1),
        GL_SAMPLER_2D_ARRAY_SHADOW: (glUniform1iv,  1),
        GL_SAMPLER_2D_MULTISAMPLE:  (glUniform1iv,  1),
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY:    (glUniform1iv,  1),
        GL_SAMPLER_CUBE_SHADOW: (glUniform1iv,  1),
        GL_SAMPLER_BUFFER:      (glUniform1iv,  1),
        GL_SAMPLER_2D_RECT:     (glUniform1iv,  1),
        GL_SAMPLER_2D_RECT_SHADOW:  (glUniform1iv,  1),
        GL_INT_SAMPLER_1D:      (glUniform1iv,  1),
        GL_INT_SAMPLER_2D:      (glUniform1iv,  1),
        GL_INT_SAMPLER_3D:      (glUniform1iv,  1),
        GL_INT_SAMPLER_CUBE:    (glUniform1iv,  1),
        GL_INT_SAMPLER_1D_ARRAY:    (glUniform1iv,  1),
        GL_INT_SAMPLER_2D_ARRAY:    (glUniform1iv,  1),
        GL_INT_SAMPLER_2D_MULTISAMPLE:  (glUniform1iv,  1),
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:    (glUniform1iv,  1),
        GL_INT_SAMPLER_BUFFER:  (glUniform1iv,  1),
        GL_INT_SAMPLER_2D_RECT: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_1D: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_2D: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_3D: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_CUBE:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_BUFFER: (glUniform1iv,  1),
        GL_UNSIGNED_INT_SAMPLER_2D_RECT:    (glUniform1iv,  1),
        GL_IMAGE_1D:            (glUniform1iv,  1),
        GL_IMAGE_2D:            (glUniform1iv,  1),
        GL_IMAGE_3D:            (glUniform1iv,  1),
        GL_IMAGE_2D_RECT:       (glUniform1iv,  1),
        GL_IMAGE_CUBE:          (glUniform1iv,  1),
        GL_IMAGE_BUFFER:        (glUniform1iv,  1),
        GL_IMAGE_1D_ARRAY:      (glUniform1iv,  1),
        GL_IMAGE_2D_ARRAY:      (glUniform1iv,  1),
        GL_IMAGE_2D_MULTISAMPLE:        (glUniform1iv,  1),
        GL_IMAGE_2D_MULTISAMPLE_ARRAY:  (glUniform1iv,  1),
        GL_INT_IMAGE_1D:        (glUniform1iv,  1),
        GL_INT_IMAGE_2D:        (glUniform1iv,  1),
        GL_INT_IMAGE_3D:        (glUniform1iv,  1),
        GL_INT_IMAGE_2D_RECT:   (glUniform1iv,  1),
        GL_INT_IMAGE_CUBE:      (glUniform1iv,  1),
        GL_INT_IMAGE_BUFFER:    (glUniform1iv,  1),
        GL_INT_IMAGE_1D_ARRAY:  (glUniform1iv,  1),
        GL_INT_IMAGE_2D_ARRAY:  (glUniform1iv,  1),
        GL_INT_IMAGE_2D_MULTISAMPLE:        (glUniform1iv,  1),
        GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY:  (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_1D:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_2D:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_3D:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_2D_RECT:  (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_CUBE: (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_BUFFER:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_1D_ARRAY: (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_2D_ARRAY: (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE:   (glUniform1iv,  1),
        GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY: (glUniform1iv,  1),
        }

    def __init__( self ):
        super( UniformSampler, self ).__init__(
            UniformSampler.types,
            'int32'
            )


class Attributes( object ):
    """Provides access to ShaderProgram attribute bindings.

    Because Attributes must be updated before the shader is linked,
    we cannot do the same validation as we can with Uniforms.

    Attributes can be accessed as members:
    shader.attributes.in_position = 0
    print shader.attributes.in_position
    >>> 0

    Attributes can also be accessed array style:
    shader.attributes[ 'in_position' ] = 0
    print shader.attributes[ 'in_position' ]
    >>> 0

    Attributes provides a mechanism to iterate over the active Attributes:
    for attribute in shader.attributes:
        print attribute
    """

    def __init__( self, program ):
        super( Attributes, self ).__init__()

        self.__dict__[ 'program' ] = program

    def _on_program_linked( self ):
        pass

    def __iter__( self ):
        return self.next()

    def next( self ):
        for attribute in self.all().values():
            yield attribute

    def all( self ):
        """Returns a dictionary of all the available attributes.

        The key is the attribute name.
        The value is an Attribute object.
        """
        # get number of active attributes
        program = self.__dict__[ 'program' ]

        _attributes = {}

        for attribute in attributes( program.handle ):
            name, size, type = attribute
            _attributes[ name ] = Attribute( program, name )

        return _attributes

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
        if name in self.__dict__:
            return self.__dict__[ name ]

        return Attribute( self.__dict__[ 'program' ], name )

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

    def __str__( self ):
        string = "Attributes:\n"
        for attribute in self:
            string += str(attribute) + "\n"
        return string[:-1]


class Attribute( object ):
    """Wraps a GLSL Vertex Attribute.
    """

    def __init__( self, program, name ):
        super( Attribute, self ).__init__()

        self._program = program
        self._name = name

    @property
    def name( self ):
        """Returns the name of the uniform as specified in GLSL.

        Eg. in_position
        """
        return self._name

    @property
    def program( self ):
        """Returns the ShaderProgram that owns the Uniform.
        """
        return self._program

    @property
    def type( self ):
        """Returns the GL enumeration type for the Attribute.

        Eg. GL_FLOAT_VEC4.
        """
        name, size, type = attribute_for_name( self.program.handle, self.name )
        return type

    @property
    def location( self ):
        """Returns the location of the Attribute.
        """
        return glGetAttribLocation( self.program.handle, self.name )

    @location.setter
    def location( self, location ):
        """Sets the attributes location.

        Locations can be set two ways:
        shader.attributes.in_position = 0
        or:
        shader.attributes.in_position.location = 0
        """
        glBindAttribLocation( self.program.handle, location, self.name )

    def __str__( self ):
        """Returns a human readable string representing the Attribute.
        """
        return "%s:\t%s\t%s\t%d" % (
            self.__class__.__name__,
            self.name,
            enum_to_string( self.type ),
            self.location
            )


# register our uniform types
def register_uniforms():
    """Registers our uniform class types with the central
    Uniforms class.

    This is called automatically on import and does not need
    to be called manually.
    Calling this multiple times will not do any harm.
    """
    Uniforms.register_uniform_class( UniformFloat, UniformFloat.types.keys() )
    Uniforms.register_uniform_class( UniformInt, UniformInt.types.keys() )
    Uniforms.register_uniform_class( UniformUint, UniformUint.types.keys() )
    Uniforms.register_uniform_class( UniformFloatMatrix, UniformFloatMatrix.types.keys() )
    Uniforms.register_uniform_class( UniformSampler, UniformSampler.types.keys() )

register_uniforms()

