from pydispatch import dispatcher


class Sender( object ):
    on_thing = 'on_thing'

    def __init__( self ):
        super( Sender, self ).__init__()

    def send_thing( self ):
        print 'sending on_thing!'
        dispatcher.send( Sender.on_thing, self, 'fhgwgads' )

class Listener( object ):

    def __init__( self ):
        super( Listener, self ).__init__()

    def on_thing( self, msg ):
        print 'on_thing received!', msg

s = Sender()
l = Listener()

dispatcher.connect( l.on_thing, s.on_thing, s )

s.send_thing()
