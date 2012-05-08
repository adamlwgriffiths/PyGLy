import unittest
import math

import numpy

from pygly.uv_generators.planar import Planar
from pyrr import vector


class test_planar( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_planar( self ):
        # ignored anyway
        normals = []
        
        vertices = numpy.array([
            [ -1.0, 1.0, 0.0 ],
            [ 0.0, 0.0, 1.0 ],
            [ 0.5, 0.0, 0.5 ],
            [ 1.0, 0.0, 1.0 ]
            ])
        
        # planer from x = 0.0 - +1.0
        # and from z = 0.0 to 1.0 
        position = numpy.array([ 0.0, 0.0, 0.0 ])
        normal = numpy.array([ 0.0, 1.0, 0.0 ])
        up = numpy.array([ 0.0, 0.0, 1.0 ])
        
        uv = Planar(
            position = position,
            normal = normal,
            up = up,
            size = (1.0, 1.0)
            )
        
        texture_coords = uv.generate_coordinates( vertices, normals )
        
        self.assertEqual(
            texture_coords[ 0 ][ 0 ],
            -1.0,
            "Planar uv coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 0 ][ 1 ],
            0.0,
            "Planar uv coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 1 ][ 0 ],
            0.0,
            "Planar uv coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 1 ][ 1 ],
            1.0,
            "Planar uv coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 2 ][ 0 ],
            0.5,
            "Planar uv coordinates incorrect"
            )
        self.assertEqual(
            texture_coords[ 2 ][ 1 ],
            0.5,
            "Planar uv coordinates incorrect"
            )


if __name__ == '__main__':
    unittest.main()

