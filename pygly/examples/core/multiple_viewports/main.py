from pygly.examples.core.simple.main import SimpleApplication

from pygly.ratio_viewport import RatioViewport


class MultipleViewportApplication( SimpleApplication ):
    
    def __init__( self ):
        super( MultipleViewportApplication, self ).__init__()

    def setup_viewports( self ):
        super( MultipleViewportApplication, self ).setup_viewports()

        # make a second viewport
        # this viewport will be 1/10th the size
        self.ratio_viewport = RatioViewport(
            self.window,
            [ [0.7, 0.7], [0.3, 0.3] ]
            )

        # we could store the viewport objects themselves
        # but for the examples we just store the actual
        # viewport rectangles
        self.viewports.append(
            self.ratio_viewport.rect
            )
        # add a colour for this viewport
        self.colours.append(
            (0.3, 0.3, 0.3, 1.0)
            )

    def on_resize( self, width, height ):
        super( MultipleViewportApplication, self ).on_resize( width, height )

        # update the viewport rectangle
        self.viewports[ 1 ] = self.ratio_viewport.rect

    def setup_cameras( self ):
        super( MultipleViewportApplication, self ).setup_cameras()

        # use the same camera for this viewport
        self.cameras.append( self.cameras[ 0 ] )


def main():
    # create app
    app = MultipleViewportApplication()
    app.run()
    app.window.close()


if __name__ == "__main__":
    main()

