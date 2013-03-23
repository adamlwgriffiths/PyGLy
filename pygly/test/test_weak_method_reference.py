import unittest
import math
import weakref

import numpy

from pygly.weak_method_reference import WeakMethodReference

called = False
test_message = 'test_message'
my_function_message = 'my_function %s'

class test_weak_method_reference( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_functions( self ):
        global called
        global my_function_message
        global test_message

        called = False

        # check that we can call our weak reference
        def my_function( message ):
            global called
            global my_function_message
            called = True
            return ( my_function_message % message )

        self.assertFalse(
            called,
            "IMPOSSIBRU!"
            )

        func_ref = WeakMethodReference( my_function )
        self.assertFalse(
            called,
            "Function called during weak ref creation"
            )
        self.assertFalse(
            func_ref.is_dead(),
            "Function reference already dead"
            )
        self.assertTrue(
            func_ref.is_alive(),
            "Function reference already dead"
            )

        result_message = func_ref()( test_message )
        self.assertTrue(
            called,
            "Function not called"
            )
        self.assertEqual(
            result_message,
            ( my_function_message % test_message ),
            "Function arguements incorrect"
            )


    def test_standard_weak_ref_methods( self ):
        # this test serves to prove that
        # the standard weak reference fails
        # with class methods

        global called
        global my_function_message
        global test_message

        called = False

        class MyClass:
            my_method_message = 'my_method %s'

            def my_method( self, message ):
                global called
                called = True
                return ( MyClass.my_method_message % message )

        obj = MyClass()
        result_message = obj.my_method( test_message )
        self.assertEqual(
            result_message,
            ( MyClass.my_method_message % test_message ),
            "Test class incorrect"
            )
        called = False

        # normal weak references dont work for object methods
        # assert that this is true
        ref = weakref.ref( obj.my_method )
        method = ref()
        self.assertEqual(
            method,
            None,
            "Standard weak reference worked with a class method!"
            )


    def test_methods( self ):
        global called
        global my_function_message
        global test_message

        called = False

        class MyClass:
            my_method_message = 'my_method %s'

            def my_method( self, message ):
                global called
                called = True
                return ( MyClass.my_method_message % message )

        obj = MyClass()

        method_ref = WeakMethodReference( obj.my_method )
        self.assertFalse(
            called,
            "Method already at creation time"
            )

        result_message = method_ref()( test_message )
        self.assertTrue(
            called,
            "Method not called"
            )
        self.assertEqual(
            result_message,
            ( MyClass.my_method_message % test_message ),
            "Method arguments incorrect"
            )

    def test_collections( self ):
        # check we can insert weak references
        # into lists, dicts, sets, etc
        # and find it through a new weak reference
        # to the same function
        global called
        global my_function_message
        global test_message

        called = False

        class MyClass:
            my_method_message = 'my_method %s'

            def my_method( self, message ):
                global called
                called = True
                return ( MyClass.my_method_message % message )

        obj = MyClass()

        method_ref = WeakMethodReference( obj.my_method )
        self.assertFalse(
            called,
            "Method already at creation time"
            )

        # check functions work
        my_function_message = 'my_function %s'
        def my_function( message ):
            global called
            global my_function_message
            called = True
            return ( my_function_message % message )

        self.assertFalse(
            called,
            "IMPOSSIBRU!"
            )

        func_ref = WeakMethodReference( my_function )

        collection = set()

        collection.add( func_ref )
        collection.add( method_ref )
        self.assertTrue(
            func_ref in collection,
            "Function ref not found in collection"
            )
        self.assertTrue(
            method_ref in collection,
            "Method ref not found in collection"
            )

        self.assertFalse(
            my_function in collection,
            "Function found in collection instead of ref"
            )
        self.assertFalse(
            obj.my_method in collection,
            "Method found in collection instead of ref"
            )

        func_ref2 = WeakMethodReference( my_function )
        method_ref2 = WeakMethodReference( obj.my_method )

        # check references are comparable
        self.assertEqual(
            func_ref,
            func_ref2,
            "Function refs not comparable"
            )
        self.assertEqual(
            method_ref,
            method_ref2,
            "Method refs not comparable"
            )
        self.assertNotEqual(
            func_ref,
            method_ref,
            "Different refs are equal"
            )


        # check copying references still works for
        # comparison operators on collections
        self.assertTrue(
            func_ref2 in collection,
            "Function ref not found in collection"
            )
        self.assertTrue(
            method_ref2 in collection,
            "Method ref not found in collection"
            )

        # remove from collection
        collection.remove( func_ref2 )
        self.assertFalse(
            func_ref in collection,
            "Function ref still in collection"
            )
        collection.remove( method_ref2 )
        self.assertFalse(
            method_ref in collection,
            "Method ref still in collection"
            )

        # ensure dead
        obj = None
        self.assertTrue(
            method_ref.is_dead(),
            "Method ref still alive after destruction"
            )
        self.assertTrue(
            method_ref2.is_dead(),
            "Copied Method ref still alive after destruction"
            )


if __name__ == '__main__':
    unittest.main()

