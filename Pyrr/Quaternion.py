'''
Created on 21/06/2011

@author: adam
'''

import math

import numpy


QuatW = 0
QuatX = 1
QuatY = 2
QuatZ = 3

# TODO: slerp, lerp

def identity( out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    out[:] = [ 1.0, 0.0, 0.0, 0.0 ]
    return out

def setToRotationAboutX( theta, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    thetaOver2 = theta * 0.5
    out[:] = [
        math.cos( thetaOver2 ),
        math.sin( thetaOver2 ),
        0,
        0
        ]
    return out

def setToRotationAboutY( theta, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    thetaOver2 = theta * 0.5
    out[:] = [
        math.cos( thetaOver2 ),
        0,
        math.sin( thetaOver2 ),
        0
        ]
    return out

def setToRotationAboutZ( theta, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    thetaOver2 = theta * 0.5
    out[:] = [
        math.cos( thetaOver2 ),
        0,
        0,
        math.sin( thetaOver2 )
        ]
    return out

def setToRotationAboutAxis( axis, theta, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    # make sure the vector is normalised
    assert (numpy.linalg.norm( axis, ord = None ) - 1.0) < 0.01
    
    thetaOver2 = theta * 0.5
    sinThetaOver2 = math.sin( thetaOver2 )
    
    out[:] = [
        math.cos( thetaOver2 ),
        axis[ 0 ] * sinThetaOver2,
        axis[ 1 ] * sinThetaOver2,
        axis[ 2 ] * sinThetaOver2
        ]
    return out

def setToRotationObjectToInertial( eulers, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    pitchOver2 = eulers[ 0 ] * 0.5
    rollOver2 = eulers[ 1 ] * 0.5
    yawOver2 = eulers[ 2 ] * 0.5
    
    sinPitch = math.sin( pitchOver2 )
    cosPitch = math.cos( pitchOver2 )
    sinRoll = math.sin( rollOver2 )
    cosRoll = math.cos( rollOver2 )
    sinYaw = math.sin( yawOver2 )
    cosYaw = math.cos( yawOver2 )
    
    out[:] = [
        # cy * cp * cr + sy * sp * sr
        (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll),
        # cy * sp * cr + sy * cp * sr
        (cosYaw * sinPitch * cosRoll) + (sinYaw * cosPitch * sinRoll),
        # -cy * sp * sr + sy * cp * cr
        (-cosYaw * sinPitch * sinRoll) + (sinYaw * cosPitch * cosRoll),
        # -sy * sp * cr + cy * cp * sr
        (-sinYaw * sinPitch * cosRoll) + (cosYaw * cosPitch * sinRoll)
        ]
    return out

def setToRotationInertialToObject( eulers, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    pitchOver2 = eulers[ 0 ] * 0.5
    rollOver2 = eulers[ 1 ] * 0.5
    yawOver2 = eulers[ 2 ] * 0.5
    
    sinPitch = math.sin( pitchOver2 )
    cosPitch = math.cos( pitchOver2 )
    sinRoll = math.sin( rollOver2 )
    cosRoll = math.cos( rollOver2 )
    sinYaw = math.sin( yawOver2 )
    cosYaw = math.cos( yawOver2 )
    
    out[:] = [
        # cy * cp * cr + sy * sp * sr
        (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll), 
        # -cy * sp * cr - sy * cp * sr
        (-cosYaw * sinPitch * cosRoll) - (sinYaw * cosPitch * sinRoll),
        # cy * sp * sr - sy * cp * cr
        (cosYaw * sinPitch * sinRoll) - (sinYaw * cosPitch * cosRoll),
        # sy * sp * cr - cy * cp * sr
        (sinYaw * sinPitch * cosRoll) - (cosYaw * cosPitch * sinRoll)
        ]
    return out

def crossProduct( quat1, quat2, out = None ):
    """
    Returns the cross-product of the two quaternions.
    Order is important.
    This is NOT the same as a vector cross-product. Quaternion cross-product
    is the equivalent of matrix multiplication.
    """
    if out == None:
        out = numpy.empty( 4, dtype = float )
    # TODO: this isn't triggering the scene node's setOrientation property function!
    out[:] = [
        # q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
        (quat1[ QuatW ] * quat2[ QuatW ]) - (quat1[ QuatX ] * quat2[ QuatX ]) - \
            (quat1[ QuatY ] * quat2[ QuatY ]) - (quat1[ QuatZ ] * quat2[ QuatZ ]),
        # q1.w * q2.x + q1.x * q2.w + q1.z * q2.y - q1.y * q2.z 
        (quat1[ QuatW ] * quat2[ QuatX ]) + (quat1[ QuatX ] * quat2[ QuatW ]) + \
            (quat1[ QuatZ ] * quat2[ QuatY ]) - (quat1[ QuatY ] * quat2[ QuatZ ]),
        # q1.w * q2.y + q1.y * q2.w + q1.x * q2.z - q1.z * q2.x
        (quat1[ QuatW ] * quat2[ QuatY ]) + (quat1[ QuatY ] * quat2[ QuatW ]) + \
            (quat1[ QuatX ] * quat2[ QuatZ ]) - (quat1[ QuatZ ] * quat2[ QuatX ]),
        # q1.w * q2.z + q1.z * q2.w + q1.y * q2.x - q1.x * q2.y
        (quat1[ QuatW ] * quat2[ QuatZ ]) + (quat1[ QuatZ ] * quat2[ QuatW ]) + \
            (quat1[ QuatY ] * quat2[ QuatX ]) - (quat1[ QuatX ] * quat2[ QuatY ]), 
        ]
    return out

def length( quat ):
    return math.sqrt(
        quat[ QuatW ]**2 + \
        quat[ QuatX ]**2 + \
        quat[ QuatY ]**2 + \
        quat[ QuatZ ]**2
        )

def normalise( quat ):
    mag = length( quat )
    if mag > 0.0:
        oneOverMag = 1.0 / mag
        quat[ QuatW ] *= oneOverMag
        quat[ QuatX ] *= oneOverMag
        quat[ QuatY ] *= oneOverMag
        quat[ QuatZ ] *= oneOverMag
    else:
        assert False
    assert 0.9 < length( quat )
    assert 1.1 > length( quat )
    #quat /= numpy.linalg.norm( quat, ord = None )
    #assert numpy.linalg.norm( quat, ord = None ) == 1.0
    return quat

def getRotationAngle( quat ):
    thetaOver2 = math.acos( quat[ QuatW ] )
    return thetaOver2 * 2.0

def getRotationAxis( quat, out = None ):
    if out == None:
        out = numpy.empty( 3, dtype = float )
    
    sinThetaOver2Sq = 1.0 - (quat[ QuatW ]**quat[ QuatW ])
    
    if sinThetaOver2Sq <= 0.0:
        # assert here for the time being
        #assert False
        print "rotation axis was identity"
        
        # identity quaternion or numerical imprecision.
        # just return a valid vector
        # we'll treat -Z as the default
        out[:] = [ 0.0, 0.0, -1.0 ]
        return out
    
    oneOverSinThetaOver2 = 1.0 / math.sqrt( sinThetaOver2Sq )
    
    out[:] = [
        quat[ QuatX ] * oneOverSinThetaOver2,
        quat[ QuatY ] * oneOverSinThetaOver2,
        quat[ QuatZ ] * oneOverSinThetaOver2
        ]
    return out

def dotProduct( quat1, quat2 ):
    return \
        (quat1[ QuatW ] * quat2[ QuatW ]) + \
        (quat1[ QuatX ] * quat2[ QuatX ]) + \
        (quat1[ QuatY ] * quat2[ QuatY ]) + \
        (quat1[ QuatZ ] * quat2[ QuatZ ])

def conjugate( quat, out = None ):
    """
    Returns a quaternion with the opposite rotation as the original quaternion
    """
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    out[:] = [
        quat[ QuatW ],
        -quat[ QuatX ],
        -quat[ QuatY ],
        -quat[ QuatZ ]
        ]
    return out

def power( quat, exponent, out = None ):
    if out == None:
        out = numpy.empty( 4, dtype = float )
    
    # check for identify quaternion
    if math.fabs( quat[ QuatW ] ) > 0.9999:
        # assert for the time being
        assert False
        print "rotation axis was identity"
        
        out[:] = quat
        return out
    
    alpha = math.acos( quat[ QuatW ] )
    newAlpha = alpha * exponent
    multi = math.sin( newAlpha ) / math.sin( alpha )
    
    out[:] = [
        math.cos( newAlpha ),
        quat[ QuatX ] * multi,
        quat[ QuatY ] * multi,
        quat[ QuatZ ] * multi
        ]
    return out


if __name__ == "__main__":
    quat = numpy.array( [0.0, 0.0, 0.0, 0.0], dtype = float )
    quat2 = quat
    
    identity( quat )
    assert quat[ QuatW ] == 1.0
    assert quat[ QuatX ] == 0.0
    assert quat[ QuatY ] == 0.0
    assert quat[ QuatZ ] == 0.0
    assert quat2 is quat
    
    quat = identity()
    assert quat[ QuatW ] == 1.0
    assert quat[ QuatX ] == 0.0
    assert quat[ QuatY ] == 0.0
    assert quat[ QuatZ ] == 0.0
    assert quat2 is not quat
    
    normalise( quat )
    assert quat[ QuatW ] == 1.0
    assert quat[ QuatX ] == 0.0
    assert quat[ QuatY ] == 0.0
    assert quat[ QuatZ ] == 0.0
    
    quat[ QuatW ] = 2.0
    normalise( quat )
    assert quat[ QuatW ] == 1.0
    assert quat[ QuatX ] == 0.0
    assert quat[ QuatY ] == 0.0
    assert quat[ QuatZ ] == 0.0
    
    del quat2
    
    
