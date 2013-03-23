from traits.api import HasTraits, Array, on_trait_change

class Parent( HasTraits ):

    thing = Array( dtype = 'float', shape = [1] )

    def __init__( self ):
        super( Parent, self ).__init__()


class ArrayTest( Parent ):
    position = Array( dtype = 'float', shape = [3] )
    scale = Array( dtype = 'float', shape = [3] )

    def __init__( self ):
        super( ArrayTest, self ).__init__()

        self.on_trait_change( self.update_position, 'thing' )

    def update_position( self ):
        self.position = [ 5.0, 5.0, 5.0 ]

    @on_trait_change( 'position' )
    def pos_changed( self, name, old, new ):
        print "pos_changed!"
        print "old", old
        print "new", new

    def _position_changed( self, old, new ):
        print "_position_changed!"
        print "old", old
        print "new", new


a = ArrayTest()
print type(a.position)

print a.position
a.position = [ 1.0, 2.0, 3.0 ]
print a.position

a.thing = [5.0]
print a.position
