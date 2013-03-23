from time import time


class FPS_Monitor( object ):

    def __init__( self, delta = 2.0 ):
        super( FPS_Monitor, self ).__init__()

        self.time = time()
        self.frame_count = 0
        self.print_time = delta

    def increment_frame( self ):
        # update our FPS
        self.frame_count += 1
        # get the latest time
        new_time = time()
        diff = new_time - self.time
        if diff > self.print_time:
            print "FPS:",float(self.frame_count) / diff
            self.time = new_time
            self.frame_count = 0
