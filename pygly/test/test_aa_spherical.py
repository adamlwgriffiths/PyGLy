import unittest
import math

import numpy

from pygly.uv_generators.aa_spherical import Spherical
import pyrr.vector as vector


class test_aa_spherical( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_spherical( self ):
        angle_vector = numpy.array([ 1.0, 0.0, 1.0 ])
        angle_vector = vector.normalise( angle_vector )
        
        normals = numpy.array([
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 1.0 ],
            [ angle_vector[ 0 ], angle_vector[ 1 ], angle_vector[ 2 ] ]
            ])
        
        uv = Spherical(
            scale = (2.0, 1.0),
            offset = (0.0, 0.0)
            )
        
        # ignored anyway
        vertices = []
        texture_coords = uv.generate_coordinates(
            vertices,
            normals
            )
        
        self.assertEqual(
            texture_coords[ 0 ][ 1 ],
            0.5,
            "UV coordinates incorrect"
            )
        # TODO check more vertices


if __name__ == '__main__':
    unittest.main()

