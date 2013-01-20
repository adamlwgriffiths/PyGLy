import unittest
import math

import numpy
import math


from pyrr import matrix44
from pyrr import vector3
from pyrr import quaternion
from pygly.scene_node import SceneNode


def test_axis( unittest, transform_space, matrix ):
    x_axis = matrix44.apply_to_vector( matrix, [1.0, 0.0, 0.0] )
    y_axis = matrix44.apply_to_vector( matrix, [0.0, 1.0, 0.0] )
    z_axis = matrix44.apply_to_vector( matrix, [0.0, 0.0, 1.0] )

    # Object space
    unittest.assertTrue(
        numpy.allclose( transform_space.x, x_axis ),
        "X axis incorrect"
        )
    unittest.assertTrue(
        numpy.allclose( transform_space.y, y_axis ),
        "Y axis incorrect"
        )
    unittest.assertTrue(
        numpy.allclose( transform_space.z, z_axis ),
        "Z axis incorrect"
        )

def test_scale( unittest, transform, scale ):
    eye = numpy.empty( 4 )
    eye[ 0:3 ] = scale
    eye[ 3 ] = 1.0

    unittest.assertTrue(
        numpy.allclose( transform.scale, scale ),
        "Scale incorrect"
        )
    unittest.assertTrue(
        numpy.allclose( numpy.diag(transform.matrix), eye ),
        "Matrix scale incorrect"
        )

def test_translation( unittest, transform, vector ):
    # Object space
    unittest.assertTrue(
        numpy.allclose( transform.translation, vector ),
        "Translation Vector incorrect"
        )

    # check the matrix translation matches the transform
    matrix_trans = vector3.create_from_matrix44_translation( transform.matrix )
    unittest.assertTrue(
        numpy.allclose( matrix_trans, vector ),
        "Translation Matrix incorrect"
        )

def test_initial_state( unittest, node ):
    matrix = matrix44.identity()

    #
    # Axis
    #
    test_axis( unittest, node.transform.object, matrix )
    test_axis( unittest, node.transform.inertial, matrix )
    test_axis( unittest, node.world_transform.object, matrix )
    test_axis( unittest, node.world_transform.inertial, matrix )

    #
    # Quaternion
    #
    quat = quaternion.identity()
    unittest.assertTrue(
        numpy.allclose( node.transform.orientation, quat ),
        "Object quaternion incorrect"
        )
    unittest.assertTrue(
        numpy.allclose( node.world_transform.orientation, quat ),
        "World quaternion incorrect"
        )

    #
    # Scale
    #
    test_scale( unittest, node.transform, [1.0, 1.0, 1.0] )
    test_scale( unittest, node.world_transform, [1.0, 1.0, 1.0] )

    #
    # Translation
    #
    test_translation( unittest, node.transform, [0.0, 0.0, 0.0] )
    test_translation( unittest, node.world_transform, [0.0, 0.0, 0.0] )


class test_list( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

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

        child1_2.remove_child( child2_2 )
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

    def test_initial_axis( self ):
        root = SceneNode( '/root' )

        test_initial_state( self, root )

    def test_child( self ):
        root = SceneNode( '/root' )
        child = SceneNode( '/child' )

        root.add_child( child )

        test_initial_state( self, root )
        test_initial_state( self, child )

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
        child = SceneNode( '/child' )
        
        root.add_child( child )

        #
        # Rotate 180 deg (1 * pi) about the Y axis (yaw)
        #
        root.transform.object.rotate_y( math.pi )

        identity = matrix44.identity()
        root_matrix = matrix44.create_from_y_rotation( math.pi )

        # root object
        test_axis( self, root.transform.object, root_matrix )
        test_axis( self, root.transform.inertial, identity )
        test_axis( self, root.world_transform.object, root_matrix )
        test_axis( self, root.world_transform.inertial, identity )

        child_matrix = matrix44.identity()
        test_axis( self, child.transform.object, child_matrix )
        test_axis( self, child.transform.inertial, identity )
        test_axis( self, child.world_transform.object, root_matrix )
        test_axis( self, child.world_transform.inertial, identity )


        # check the node matrix matches what we're seeing in
        # the transform axis values
        self.assertTrue(
            numpy.allclose( root.transform.matrix, root_matrix ),
            "Root Local Matrix incorrect"
            )
        self.assertTrue(
            numpy.allclose( root.world_transform.matrix, root_matrix ),
            "Root RootMatrix incorrect"
            )

        self.assertTrue(
            numpy.allclose( child.transform.matrix, identity ),
            "Child Local Matrix incorrect"
            )
        self.assertTrue(
            numpy.allclose( child.world_transform.matrix, root_matrix ),
            "Child RootMatrix incorrect"
            )


        #
        # Rotate 180 deg (1 * pi) about the X axis (pitch)
        #
        # rotate 180 deg / 1pi about the x axis (pitch)
        child.transform.object.rotate_x( math.pi )

        child_matrix = matrix44.multiply(
            matrix44.create_from_x_rotation( math.pi ),
            child_matrix
            )

        child_world = matrix44.multiply( child_matrix, root_matrix )

        # root object
        test_axis( self, root.transform.object, root_matrix )
        test_axis( self, root.transform.inertial, identity )
        test_axis( self, root.world_transform.object, root_matrix )
        test_axis( self, root.world_transform.inertial, identity )

        test_axis( self, child.transform.object, child_matrix )
        test_axis( self, child.transform.inertial, identity )
        test_axis( self, child.world_transform.object, child_world )
        test_axis( self, child.world_transform.inertial, identity )

        # check the node matrix matches what we're seeing in
        # the transform axis values
        self.assertTrue(
            numpy.allclose( root.transform.matrix, root_matrix ),
            "Root Local Matrix incorrect"
            )
        self.assertTrue(
            numpy.allclose( root.world_transform.matrix, root_matrix ),
            "Root RootMatrix incorrect"
            )

        self.assertTrue(
            numpy.allclose( child.transform.matrix, child_matrix ),
            "Child Local Matrix incorrect"
            )
        self.assertTrue(
            numpy.allclose( child.world_transform.matrix, child_world ),
            "Child RootMatrix incorrect"
            )


    def test_scale( self ):
        root = SceneNode( '/root' )
        child = SceneNode( '/child' )
        
        root.add_child( child )

        #
        # Initial state
        #
        test_scale( self, root.transform, [1.0, 1.0, 1.0] )
        test_scale( self, root.world_transform, [1.0, 1.0, 1.0] )
        test_scale( self, child.transform, [1.0, 1.0, 1.0] )
        test_scale( self, child.world_transform, [1.0, 1.0, 1.0] )

        #
        # Root Scale = 2.0
        #
        root.transform.scale = [2.0, 2.0, 2.0]
        test_scale( self, root.transform, [2.0, 2.0, 2.0] )
        test_scale( self, root.world_transform, [2.0, 2.0, 2.0] )
        test_scale( self, child.transform, [1.0, 1.0, 1.0] )
        test_scale( self, child.world_transform, [2.0, 2.0, 2.0] )

        #
        # Child World Scale = 2.0
        #
        child.world_transform.scale = [1.0, 1.0, 1.0]
        test_scale( self, root.transform, [2.0, 2.0, 2.0] )
        test_scale( self, root.world_transform, [2.0, 2.0, 2.0] )
        test_scale( self, child.transform, [0.5, 0.5, 0.5] )
        test_scale( self, child.world_transform, [1.0, 1.0, 1.0] )

        #
        # Root Scale = 1.0
        #
        root.transform.scale = [1.0, 1.0, 1.0]
        test_scale( self, root.transform, [1.0, 1.0, 1.0] )
        test_scale( self, root.world_transform, [1.0, 1.0, 1.0] )
        test_scale( self, child.transform, [0.5, 0.5, 0.5] )
        test_scale( self, child.world_transform, [0.5, 0.5, 0.5] )

    def test_translation( self ):
        root = SceneNode( '/root' )
        child = SceneNode( '/child' )
        
        root.add_child( child )

        #
        # Initial state
        #
        test_translation( self, root.transform, [0.0, 0.0, 0.0] )
        test_translation( self, root.world_transform, [0.0, 0.0, 0.0] )
        test_translation( self, child.transform, [0.0, 0.0, 0.0] )
        test_translation( self, child.world_transform, [0.0, 0.0, 0.0] )

        #
        # Root Translate += 1.0, 1.0, 1.0
        #
        root.transform.translation += [1.0, 1.0, 1.0]
        test_translation( self, root.transform, [1.0, 1.0, 1.0] )
        test_translation( self, root.world_transform, [1.0, 1.0, 1.0] )
        test_translation( self, child.transform, [0.0, 0.0, 0.0] )
        test_translation( self, child.world_transform, [1.0, 1.0, 1.0] )

        #
        # Child Translate -= 1.0, 1.0, 1.0
        #
        child.transform.translation -= [1.0, 1.0, 1.0]
        test_translation( self, root.transform, [1.0, 1.0, 1.0] )
        test_translation( self, root.world_transform, [1.0, 1.0, 1.0] )
        test_translation( self, child.transform, [-1.0,-1.0,-1.0] )
        test_translation( self, child.world_transform, [0.0, 0.0, 0.0] )

    def test_translation_with_rotation( self ):
        root = SceneNode( '/root' )
        child = SceneNode( '/child' )
        
        root.add_child( child )

        #
        # Rotate 180 deg (1 * pi) about the Y axis (yaw)
        #
        root.transform.object.rotate_y( math.pi )

        identity = matrix44.identity()
        root_matrix = matrix44.create_from_y_rotation( math.pi )

        #
        # Translate the child node
        #
        child.transform.translation = [1.0, 1.0, 1.0]

        test_translation( self, root.transform, [0.0, 0.0, 0.0] )
        test_translation( self, root.world_transform, [0.0, 0.0, 0.0] )
        test_translation( self, child.transform, [1.0, 1.0, 1.0] )
        # Y does not invert
        test_translation( self, child.world_transform, [-1.0, 1.0,-1.0] )



if __name__ == '__main__':
    unittest.main()

