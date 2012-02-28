'''
Created on 29/05/2011

@author: adam
'''

import numpy
import numpy.linalg

import Pyrr.Vector.Vector as Vector 


class Plane( object ):
    
    
    def __init__( self, position, normal, up  ):
        """
        Creates a plane at position with the normal being above the plane
        and up being
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
        
        Vector.normalise( self.normal )
        Vector.normalise( self.up )
        
        if numpy.dot( self.normal, self.up ) != 0.0:
            raise ValueError( "Vectors are not co-planar" )
    
    def flipNormal( self ):
        self.normal *= -1
    
    def heightAbovePlane( self, vector ):
        """
        Returns the height above the plane.
        Performs no checking of the vector being within the plane's surface
        if one is defined.
        
        @return: The height above the plane as a float
        """
        planeDot = numpy.dot( self.normal, self.position )
        vectorDot = numpy.dot( vector, self.normal )
        return vectorDot - planeDot 
    
    def closestPointOnPlane( self, vector ):
        """
        point on plane is defined as:
        q' = q + (d - q.n)n
        where:
        q' is the point on the plane
        q is the point we are checking
        d is the value of normal dot position
        n is the plane normal
        """
        planeDot = numpy.dot( self.normal, self.position )
        vectorDot = numpy.dot( vector, self.normal )
        return vector + (  self.normal * (planeDot - vectorDot) )
        
    

def createPlane( vector1, vector2, vector3 ):
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
    
    projection = plane.closestPointOnPlane( vector )
    print "projection: %s" % str(projection)
    
    
    # create plane
    vectors = numpy.array([
        [ 0.0, 0.0, 1.0 ],
        [ 1.0, 0.0, 1.0 ],
        [ 0.0, 1.0, 1.0 ]
        ])
    newPlane = createPlane( vectors[ 0 ], vectors[ 1 ], vectors[ 2 ] )
    print "plane position: %s" % str(newPlane.position)
    print "plane normal: %s" % str(newPlane.normal)
    
    newPlane.flipNormal()
    print "plane position: %s" % str(newPlane.position)
    print "plane normal: %s" % str(newPlane.normal)
    
    
    # distance
    distanceVector = numpy.array([ 0.0, 0.0, 20.0 ])
    distance = newPlane.heightAbovePlane( distanceVector )
    # should be 19.0
    print "distance: %f" % distance
    assert distance == 19.0
    
    
    closestPoint = newPlane.closestPointOnPlane( distanceVector )
    # should be # 0, 0, 1
    print "closestPoint: %s" % str(closestPoint)
    assert closestPoint[ 0 ] == 0.0
    assert closestPoint[ 1 ] == 0.0
    assert closestPoint[ 2 ] == 1.0
    

