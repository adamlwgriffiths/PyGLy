import unittest
import math

import numpy
import pyglet

import pygly.list


class test_viewport( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_list_equivalent( self ):
        self.assertTrue(
            pygly.list.are_equivalent(
                [1,2,3],
                [1,2,3]
                ),
            "List equivalent failed with similar lists"
            )
        self.assertFalse(
            pygly.list.are_equivalent(
                [1,2,3],
                [1,3,2]
                ),
            "List equivalent failed with different lists"
            )
        self.assertFalse(
            pygly.list.are_equivalent(
                [1,2,3],
                [4,5,6]
                ),
            "List equivalent failed with different lists"
            )

    def test_not_equivalent( self ):
        self.assertTrue(
            pygly.list.not_equivalent(
                [-1,-1],
                [ 0, 0]
                ),
            "List not equivalent failed with different lists"
            )
        self.assertFalse(
            pygly.list.not_equivalent(
                [1,2,3],
                [1,2,3]
                ),
            "List not equivalent failed with similar lists"
            )

if __name__ == '__main__':
    unittest.main()

