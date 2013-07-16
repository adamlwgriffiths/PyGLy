import textwrap
import os

from OpenGL import GL
from PIL import Image

import pyrr.rectangle
import pyrr.matrix44
import pygly.gl
import pygly.viewport
from pygly.texture import Texture2D

import scene
import renderable_textured_quad


class Scene( scene.Scene ):

    def __init__( self, core_profile = True ):
        super( Scene, self ).__init__( core_profile )

    @property
    def name( self ):
        return "Basic"

    def initialise( self ):
        super( Scene, self ).initialise()

        # create a viewport
        # this will be updated before we begin
        self.viewport = None

        # create our projection matrix
        # this will be updated before we begin rendering
        self.projection_matrix = None

        # create a quad to render
        self.quad = renderable_textured_quad.create( self.core_profile )

        # move the quad back
        self.transform = pyrr.matrix44.create_from_translation(
            [ 0.0, 0.0,-3.0 ]
            )

        # create our textures
        self.textures = []
        self.current_texture = 0

        # load some from a directory using PIL
        image_directory = os.path.join( os.path.dirname( __file__ ), 'data/textures' )
        self.load_texture_directory(image_directory)

        # generate some random ones using numpy
        self.generate_random_textures()

    def load_texture_directory( self, directory ):
        print 'Loading images from', directory

        extensions = [
            '.png',
            '.jpg',
            '.jpeg',
            '.tif',
            '.bmp',
            '.exr',
            ]

        for filename in os.listdir( directory ):
            name, extension = os.path.splitext( filename )

            if extension not in extensions:
                continue

            try:
                print filename,
                full_path = '%s/%s' % (directory, filename)
                texture = Texture2D.from_file(full_path)
                self.textures.append((filename, texture))
            except Exception as e:
                print 'Exception:', e
                # ensure we unbound our textures
                GL.glBindTexture( GL.GL_TEXTURE_2D, 0 )

    def generate_random_textures( self ):
        import numpy

        def float32_rgb():
            data = numpy.linspace(0.0, 1.0, 32 * 32 * 3).astype('float32')
            data.shape = (32,32,-1)
            texture = Texture2D(data=data)
            return texture

        self.textures.append(('Gradient RGB (float32)', float32_rgb()))

        def uint8_rgb():
            data = numpy.linspace(0, 255, 32 * 32 * 3).astype('uint8')
            data.shape = (32,32,-1)
            texture = Texture2D(data=data)
            return texture

        self.textures.append(('Gradient RGB (uint8)', uint8_rgb()))

        def random_rgb():
            data = numpy.random.random_integers(0, 255, 32 * 32 * 3).astype('uint8')
            data.shape = (32,32,-1)
            texture = Texture2D(data=data)
            return texture

        self.textures.append(('Random RGB (uint8)', random_rgb()))

        def random_luminance():
            data = numpy.random.random_integers(0, 255, 32 * 32).astype('uint8')
            data.shape = (32,32,-1)

            from pygly import gl
            if gl.is_legacy():
                texture = Texture2D(data=data, internal_format=GL.GL_LUMINANCE)
            else:
                texture = Texture2D(data=data, swizzle='rrr', internal_format=GL.GL_RGB)
            return texture

        self.textures.append(('Random Luminance (uint32)', random_luminance()))

        """
        def random_rgb():
            # create a random RGB texture
            name = 'Red Shade RGB'
            format = 'u8/rgb/rgb8'
            print name, format
            data = numpy.linspace( 0, 255, 32 * 32 * 3 )
            data.shape = (-1,3)
            data[:,1:3] = 0.0
            texture = Texture2D()
            texture.bind()
            texture.set_min_mag_filter( GL.GL_NEAREST, GL.GL_NEAREST )
            texture.set_image(
                data.astype('uint8').flat,
                (32,32),
                format
                )
            texture.unbind()
            self.textures.append( (name, texture) )
        random_rgb()

        def random_luminance():
            # create a random luminance texture
            name = 'Random Luminance'
            format = 'u8/r/rgba8/rrr1'
            print name, format
            data = numpy.random.random_integers( 120, 255, 32 * 32 )
            texture = Texture2D()
            texture.bind()
            texture.set_min_mag_filter( GL.GL_NEAREST, GL.GL_NEAREST )
            texture.set_image(
                data.astype('uint8').flat,
                (32,32),
                format
                )
            texture.unbind()
            self.textures.append( (name, texture) )
        random_luminance()
        """

    def on_key_pressed( self, key ):
        if key == "right":
            self.current_texture += 1
            self.current_texture %= len( self.textures )

            name, texture = self.textures[ self.current_texture ]
            print name, texture.internal_format
        elif key == "left":
            self.current_texture -= 1
            if self.current_texture < 0:
                self.current_texture = len( self.textures ) - 1

            name, texture = self.textures[ self.current_texture ]
            print name, texture.internal_format

    def on_window_resized( self, width, height ):
        # update the viewport
        self.viewport = pyrr.rectangle.create_from_position(
            x = 0,
            y = 0,
            width = width,
            height = height
            )

        # update the projection matrix
        # we need to do this or the rendering will become skewed with each
        # resize of viewport change
        aspect_ratio = pyrr.rectangle.aspect_ratio( self.viewport )
        self.projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(
            fovy = 80.0,
            aspect = aspect_ratio,
            near = 1.0,
            far = 100.0
            )

    def render( self ):
        super( Scene, self ).render()

        def render_core():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            GL.glActiveTexture( GL.GL_TEXTURE0 )
            texture = self.textures[ self.current_texture ][ 1 ]
            texture.bind()
            self.quad.draw( self.projection_matrix, self.transform )
            texture.unbind()

        def render_legacy():
            # activate our viewport
            pygly.viewport.set_viewport( self.viewport )

            GL.glActiveTexture( GL.GL_TEXTURE0 )
            texture = self.textures[ self.current_texture ][ 1 ]
            texture.bind()
            with pygly.gl.mode_and_matrix(
                GL.GL_PROJECTION,
                self.projection_matrix
                ):
                with pygly.gl.mode_and_matrix(
                    GL.GL_MODELVIEW,
                    self.transform
                    ):
                    self.quad.draw()
            texture.unbind()

        # setup the projection and model view matrices
        # and draw the triangle
        if self.core_profile:
            render_core()
        else:
            render_legacy()

