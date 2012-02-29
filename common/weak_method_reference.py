'''
Created on 29/02/2012

@author: adam
'''

import weakref


class WeakMethodReference( object ):
    """
    http://stackoverflow.com/questions/6975508/can-i-weak-reference-methods
    """
    
    def __init__(self, method = None ):
        super( WeakMethodReference, self).__init__()
        
        self.set_method( method )
    
    def set_method( self, method ):
        self.object = None
        self.method = None
        if method != None:
            self.object = weakref.ref( method.im_self )
            self.method = weakref.ref( method.im_func )

    def is_valid( self ):
        return self.object != None and self.method != None

    def dereference( self ):
        if self.object == None or self.method == None:
            return None

        obj = self.object()
        function = self.method()

        method = getattr( obj, function.__name__ )
        return method
    
    def __call__( self ):
        """Return a pair containing the referent and the number of
        times the reference has been called.
        """
        return self.dereference()
    

if __name__ == '__main__':
    called = False

    class MyClass:
        def my_method( self ):
            global called
            print 'called!'
            called = True

    obj = MyClass()

    # normal weak references dont work for object methods
    # assert that this is true
    normal_weak_reference = weakref.ref( obj.my_method )
    method = normal_weak_reference()
    assert method == None

    # try our fixed version
    weak_method = WeakMethodReference( obj.my_method )
    assert called == False
    func = weak_method()
    func()
    assert called == True
