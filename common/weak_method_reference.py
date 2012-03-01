'''
Provides an implementation of a WeakMethodReference
for weak references to functions and methods.

The standard weakref module in Python cannot store
references to non-bound functions and should not
be used to perform this task.

Code borrowed from the following places:
http://code.activestate.com/recipes/81253/
http://stackoverflow.com/questions/3942303/how-does-a-python-set-check-if-two-objects-are-equal-what-methods-does-an-o

Created on 29/02/2012

@author: adam
'''

import weakref
import new


class WeakMethodReference( object ):
    """
    Stores a reference to an object's method or a
    function.

    This class also provides comparison operators to
    allow proper usage in containers such as set([]).

    The ability to change the weak reference is not
    supported to prevent mutability. This is important
    for container support as the object hash would
    change after storing it.
    """

    def __init__(self, function = None ):
        """
        Initialises the weak reference with
        a function or class method.
        """
        super( WeakMethodReference, self ).__init__()

        try:
            if function.im_self is not None:
                # bound method
                self._obj = weakref.ref( function.im_self )
            else:
                # unbound method
                self._obj = None
            self._func = function.im_func
            self._class = function.im_class
        except AttributeError:
            # not a method
            self._obj = None
            self._func = function
            self._class = None

    def __call__( self ):
        """
        @return Returns a new bound-method like the original, or
        the original function if refers just to a function or
        unbound method.
        Returns None if the original object doesn't exist
        """
        if self.is_dead():
            return None
        if self._obj is not None:
            # we have an instance: return a bound method
            return new.instancemethod(
                self._func,
                self._obj(),
                self._class
                )
        else:
            # we don't have an instance: return just the
            # function
            return self._func

    def is_dead( self ):
        """
        Returns True if the referenced callable was a bound method and
        the instance no longer exists. Otherwise, return False.
        """
        if self._obj is None and self._func is not None:
            return False
        if self._obj is not None and self._obj() is None:
            return True
        return False

    def is_alive( self ):
        """
        The equivalent to 'not is_dead()'
        Make a positive method call because
        double negatives suck
        """
        return not self.is_dead()

    def __eq__( self, other ):
        """
        Enables comparison between different weak
        pointer objects that point to the same
        object based on the contents instead of the
        object pointer.
        """
        return (
            isinstance(other, self.__class__ ) \
            and self.__dict__ == other.__dict__
            )

    def __ne__( self, other ):
        """
        Enables comparison between different weak
        pointer objects that point to the same
        object based on the contents instead of the
        object pointer.
        """
        return not self.__eq__(other)

    def __hash__( self ):
        """
        this method is provided to allow comparison of
        references inside of containers like set([])
        http://stackoverflow.com/questions/3942303/how-does-a-python-set-check-if-two-objects-are-equal-what-methods-does-an-o
        """
        return hash( (self._obj, self._func, self._class) )


if __name__ == '__main__':
    # check that we can call our weak reference
    called = False
    test_message = 'test_message'

    # check functions work
    my_function_message = 'my_function %s'
    def my_function( message ):
        global called
        global my_function_message
        called = True
        return ( my_function_message % message )

    assert called == False
    print 'creating function reference'
    func_ref = WeakMethodReference( my_function )
    assert called == False
    assert func_ref.is_dead() == False
    assert func_ref.is_alive() == True
    print 'calling function'
    result_message = func_ref()( test_message )
    assert called == True
    assert result_message == ( my_function_message % test_message )


    # test class methods
    class MyClass:
        my_method_message = 'my_method %s'

        def my_method( self, message ):
            global called
            called = True
            return ( MyClass.my_method_message % message )

    obj = MyClass()
    result_message = obj.my_method( test_message )
    assert result_message == ( MyClass.my_method_message % test_message )
    called = False

    # normal weak references dont work for object methods
    # assert that this is true
    ref = weakref.ref( obj.my_method )
    method = ref()
    assert method == None

    # try our fixed version
    print 'creating method reference'
    method_ref = WeakMethodReference( obj.my_method )
    assert called == False
    print 'calling dereferenced method'
    result_message = method_ref()( test_message )
    print result_message
    assert called == True
    assert result_message == ( MyClass.my_method_message % test_message )

    # check we can insert weak references
    # into lists, dicts, sets, etc
    # and find it through a new weak reference
    # to the same function
    print 'adding references to collection'
    collection = set()

    collection.add( func_ref )
    collection.add( method_ref )
    assert func_ref in collection
    assert method_ref in collection
    print 'checking normal method does not match reference'
    assert my_function not in collection
    assert obj.my_method not in collection

    func_ref2 = WeakMethodReference( my_function )
    method_ref2 = WeakMethodReference( obj.my_method )

    print 'checking references to the same object are comparable'
    assert func_ref == func_ref2
    assert method_ref == method_ref2
    assert func_ref != method_ref

    print 'checking new reference objects match existing ones'

    assert func_ref2 in collection
    assert method_ref2 in collection

    obj = None
    assert method_ref.is_dead() == True
    assert method_ref2.is_dead() == True

