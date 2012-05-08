import unittest
import math

import numpy
import math

from pygly.scene_node import SceneNode
import pygly.list


def compare_float_vector( a, b, tolerance = 0.1 ):
    for i, j in zip( a, b ):
        if (i - tolerance) > j:
            return False
        if (i + tolerance) < j:
            return False
    return True

class test_list( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_compare_function( self ):
        # test our above test function
        # test-ception
        self.assertTrue(
            compare_float_vector( [1.0,0.0], [1.0,0.0] ),
            "Compare function failed, tests unreliable"
            )
        self.assertFalse(
            compare_float_vector( [1.0,0.0], [0.0,1.0] ),
            "Compare function failed, tests unreliable"
            )
        self.assertTrue(
            compare_float_vector( [1.0,0.0], [1.01,0.0] ),
            "Compare function failed, tests unreliable"
            )
        self.assertFalse(
            compare_float_vector( [1.0,0.0], [1.11,0.0] ),
            "Compare function failed, tests unreliable"
            )

    def test_tree( self ):
        root = SceneNode( 'root' )

        child1_1 = SceneNode( 'child1_1' )
        child1_2 = SceneNode( 'child1_2' )

        child2_1 = SceneNode( 'child2_1' )
        child2_2 = SceneNode( 'child2_2' )

        root.add_child( child1_1 )
        root.add_child( child1_2 )

        child1_1.add_child( child2_1 )
        child1_2.add_child( child2_2 )

        self.assertTrue(
            child1_1.parent is root,
            "Parent not set correctly"
            )
        self.assertTrue(
            child1_1 in root.children,
            "Child not in parents child list"
            )
        self.assertTrue(
            child1_2.parent is root,
            "Parent not set correctly"
            )
        self.assertTrue(
            child1_2 in root.children,
            "Child not in parents child list"
            )

        self.assertTrue(
            child2_1.parent is child1_1,
            "Parent not set correctly"
            )
        self.assertTrue(
            child2_1 in child1_1.children,
            "Child not in parents child list"
            )
        self.assertTrue(
            child2_2.parent is child1_2,
            "Parent not set correctly"
            )
        self.assertTrue(
            child2_2 in child1_2.children,
            "Child not in parents child list"
            )

        child1_1.add_child( child2_2 )

        self.assertTrue(
            child2_2.parent is child1_1,
            "Parent not set correctly"
            )
        self.assertTrue(
            child2_2 in child1_1.children,
            "Child not in parents child list"
            )
        self.assertFalse(
            child2_2 in child1_2.children,
            "Child not removed from parents child list"
            )

    def test_rotation( self ):
        """
        Rotation and Inheritance
        """

        # we'll add a child to a root node
        # we'll move the child
        # rotate the root
        # and check the child is where it should be
        # the child should be moved somewhere that will
        # make it easy to check

        root = SceneNode( '/root' )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_x_axis(),
                [1.0,0.0,0.0]
                ),
            "X axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Y axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Z axis incorrect"
            )

        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_x_axis(),
                [1.0,0.0,0.0]
                ),
            "World x axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "World y axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "World z axis incorrect"
            )

        child = SceneNode( '/child' )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Child x axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child y axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child z axis incorrect"
            )

        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Child world x axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child world y axis incorrect"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child world z axis incorrect"
            )

        root.add_child( child )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Root x axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Root y axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Root z axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Root world x axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Root world y axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Root world z axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Child x axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child y axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child z axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Child world x axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child world y axis moved"
            )
        self.assertTrue(
            pygly.list.are_equivalent(
                child.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child world z axis moved"
            )

        # rotate 180 deg / 1pi about the y axis (yaw)
        root.rotate_object_y( math.pi )
        # ensure the object x axis has rotated to the left
        self.assertTrue(
            compare_float_vector(
                root.object_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Root x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Root y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.object_z_axis(),
                [0.0,0.0,-1.0]
                ),
            "Root z axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Root world x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Root world y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_z_axis(),
                [0.0,0.0,-1.0]
                ),
            "Root world z axis incorrect after rotation"
            )
        # ensure the child's object x axis has remaind unchanged
        self.assertTrue(
            compare_float_vector(
                child.object_x_axis(),
                [1.0,0.0,0.0]
                ),
            "Child x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child z axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Child world x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child world y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_z_axis(),
                [0.0,0.0,-1.0]
                ),
            "Child world z axis incorrect after rotation"
            )

        # rotate 180 deg / 1pi about the x axis (pitch)
        root.rotate_object_x( math.pi )
        # ensure the object y axis has inverted to the bottom
        # the z axis will have inverted again
        self.assertTrue(
            compare_float_vector(
                root.object_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Root x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.object_y_axis(),
                [0.0,-1.0,0.0]
                ),
            "Root y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Root z axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Root world x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_y_axis(),
                [0.0,-1.0,0.0]
                ),
            "Root world y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                root.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Root world z axis incorrect after rotation"
            )
        # ensure the child's object y axis has remaind unchanged
        self.assertTrue(
            compare_float_vector(
                child.object_x_axis(), 
                [1.0,0.0,0.0]
                ),
            "Child x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.object_y_axis(),
                [0.0,1.0,0.0]
                ),
            "Child y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.object_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child z axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_x_axis(),
                [-1.0,0.0,0.0]
                ),
            "Child world x axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_y_axis(),
                [0.0,-1.0,0.0]
                ),
            "Child world y axis incorrect after rotation"
            )
        self.assertTrue(
            compare_float_vector(
                child.world_z_axis(),
                [0.0,0.0,1.0]
                ),
            "Child world z axis incorrect after rotation"
            )

    def test_scale( self ):
        root = SceneNode( '/root' )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.scale,
                [1.0,1.0,1.0]
                ),
            "Initial scale incorrect"
            )

        root.set_scale( [2.0, 2.0, 2.0] )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.scale,
                [2.0,2.0,2.0]
                ),
            "Scale incorrect after adjustment"
            )

        root.set_scale( [1.0, 1.0, 1.0] )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.scale,
                [1.0,1.0,1.0]
                ),
            "Scale incorrect after adjustment"
            )

        root.apply_scale( [2.0, 2.0, 2.0] )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.scale,
                [2.0,2.0,2.0]
                ),
            "Scale incorrect after adjustment"
            )

        root.apply_scale( [2.0, 2.0, 2.0] )
        self.assertTrue(
            pygly.list.are_equivalent(
                root.scale,
                [4.0,4.0,4.0]
                ),
            "Scale incorrect after adjustment"
            )


if __name__ == '__main__':
    unittest.main()

