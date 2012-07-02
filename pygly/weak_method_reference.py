'''
Provides an implementation of a WeakMethodReference
for weak references to functions and methods.

The standard weakref module in Python cannot store
references to non-bound functions and should not
be used to perform this task.

Code borrowed from the following places:
http://code.activestate.com/recipes/81253/
http://stackoverflow.com/questions/3942303/how-does-a-python-set-check-if-two-objects-are-equal-what-methods-does-an-o

.. moduleauthor:: Adam Griffiths <adam.lw.griffiths@gmail.com>
'''

import weakref
import new


class WeakMethodReference( object ):
    """Provides the ability to store a weak pointer to
    class members on top of the existing weakref functionality
    provided by python.

    This class also provides comparison operators to
    allow proper usage in containers such as set([]).

    The ability to change the weak reference is not
    supported to prevent mutability. This is important
    for container support as the object hash would
    change after storing it.
    """

    def __init__(self, function = None ):
        """Initialises the weak reference with
        a function or class method.

        Args:
            function: The object to store a weak reference to.
            This can be a class, object, method or function.
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
        Returns:
            Returns a new bound-method like the original, or
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
        """Check if the referenced object is invalid.

        Returns:
            True if the referenced callable was a bound method and
            the instance no longer exists. Otherwise, return False.
        """
        if self._obj is None and self._func is not None:
            return False
        if self._obj is not None and self._obj() is None:
            return True
        return False

    def is_alive( self ):
        """Check if the referenced object is valid.

        The equivalent to 'not is_dead()'
        Make a positive method call because double negatives suck
        """
        return not self.is_dead()

    def __eq__( self, other ):
        """Provides an 'equal' operator.

        .. note::
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
        """Provides a 'not-equal' operator.

        .. note::
            Enables comparison between different weak
            pointer objects that point to the same
            object based on the contents instead of the
            object pointer.
        """
        return not self.__eq__(other)

    def __hash__( self ):
        """Generates a hash value for the stored reference.

        .. note::
            This method is provided to allow comparison of
            references inside of containers like set([])
            http://stackoverflow.com/questions/3942303/how-does-a-python-set-check-if-two-objects-are-equal-what-methods-does-an-o
        """
        return hash( (self._obj, self._func, self._class) )

