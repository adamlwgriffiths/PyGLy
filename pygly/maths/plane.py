'''
Created on 29/05/2011

@author: adam
'''

import numpy
import numpy.linalg

import maths.vector


class Plane( object ):
    
    
    def __init__( self, position, normal, up  ):
        """
        Creates a plane at position with the normal being above the plane
        and up being the rotation of the plane.
        This is required as a plane must be defined by
        3 vectors otherwise rotation is undefined.

        @param position: Must be a numpy array
        @param normal: Must be a numpy array. The normal will be normalised
        during construction.
        @param up: Must be a numpy array and must be co-planar. The up vector
        will be normalised during construction.
        @raise ValueError: raised if the up vector is not co-planar
        """
        super( Plane, self ).__init__()
        
        self.position = numpy.array( position, dtype = float )
        self.normal = numpy.array( normal, dtype = float )
        self.up = numpy.array( up, dtype = float )
        
        maths.vector.normalise( self.normal )
        maths.vector.normalise( self.up )
        
        if numpy.dot( self.normal, self.up ) != 0.0:
            raise ValueError( "Vectors are not co-planar" )
    
    def flip_normal( self ):
        self.normal *= -1
    
    def height_above_plane( self, vector ):
        """
        Returns the height above the plane.
        Performs no checking of the vector being within the plane's surface
        if one is defined.
        
        @return: The height above the plane as a float
        """
        plane_dot = numpy.dot( self.normal, self.position )
        vector_dot = numpy.dot( vector, self.normal )
        return vector_dot - plane_dot 
    
    def closest_point_on_plane( self, vector ):
        """
        point on plane is defined as:
        q' = q + (d - q.n)n
        where:
        q' is the point on the plane
        q is the point we are checking
        d is the value of normal dot position
        n is the plane normal
        """
        plane_dot = numpy.dot( self.normal, self.position )
        vector_dot = numpy.dot( vector, self.normal )
        return vector + (  self.normal * (plane_dot - vector_dot) )
        
    

def create_plane( vector1, vector2, vector3 ):
    """
    Create a plane from 3 co-planar vectors.
    The vectors must all lie on the same
    plane or an exception will be thrown.
    @raise ValueError:  raised if the vectors
    are not co-planar.
    """
    # make the vectors relative to vector2
    relV1 = vector1 - vector2
    relV2 = vector3 - vector2
    
    # cross our relative vectors
    normal = numpy.cross( relV1, relV2 )
    
    # create our plane
    return Plane(
        position = vector2,
        normal = normal,
        up = relV1
        )
    


if __name__ == "__main__":
    plane = Plane(
        position = [0.0, 0.0, 0.0],
        normal = [0.0, 0.0, 1.0],
        up = [1.0, 0.0, 0.0]
        )
    
    vector = numpy.array([ [1.0, 1.0, 1.0] ])
    
    projection = plane.closest_point_on_plane( vector )
    print "projection: %s" % str(projection)
    
    
    # create plane
    vectors = numpy.array([
        [ 0.0, 0.0, 1.0 ],
        [ 1.0, 0.0, 1.0 ],
        [ 0.0, 1.0, 1.0 ]
        ])
    new_plane = create_plane( vectors[ 0 ], vectors[ 1 ], vectors[ 2 ] )
    print "plane position: %s" % str(new_plane.position)
    print "plane normal: %s" % str(new_plane.normal)
    
    new_plane.flip_normal()
    print "plane position: %s" % str(new_plane.position)
    print "plane normal: %s" % str(new_plane.normal)
    
    
    # distance
    distance_vector = numpy.array([ 0.0, 0.0, 20.0 ])
    distance = new_plane.height_above_plane( distance_vector )
    # should be 19.0
    print "distance: %f" % distance
    assert distance == 19.0
    
    
    closest_point = new_plane.closest_point_on_plane( distance_vector )
    # should be # 0, 0, 1
    print "closestPoint: %s" % str(closest_point)
    assert closest_point[ 0 ] == 0.0
    assert closest_point[ 1 ] == 0.0
    assert closest_point[ 2 ] == 1.0
    

