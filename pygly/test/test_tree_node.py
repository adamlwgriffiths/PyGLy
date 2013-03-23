import unittest
import math

import numpy

from pygly.tree_node import TreeNode


class test_node( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_node_dfs( self ):
        # tier 1
        a1 = TreeNode()

        # tier 2
        tier2 = []

        node = TreeNode()
        node.name = "b1"
        tier2.append( node )

        node = TreeNode()
        node.name = "b2"
        tier2.append( node )

        # tier 3
        tier3 = []

        node = TreeNode()
        node.name = "c1"
        tier3.append( node )

        node = TreeNode()
        node.name = "c2"
        tier3.append( node )

        node = TreeNode()
        node.name = "c3"
        tier3.append( node )

        node = TreeNode()
        node.name = "c4"
        tier3.append( node )

        # a1 -> tier2
        a1.add_child( tier2[ 0 ] )
        a1.add_child( tier2[ 1 ] )

        # tier 3
        tier2[ 0 ].add_child( tier3[ 0 ] )
        tier2[ 0 ].add_child( tier3[ 1 ] )
        tier2[ 1 ].add_child( tier3[ 2 ] )
        tier2[ 1 ].add_child( tier3[ 3 ] )

        dfs = [ node for node in a1.dfs() ]
        for node in dfs:
            print node.name

        try:
            dfs = a1.dfs()
            child = dfs.next()
            while child:
                print child.name
                child = dfs.next()
        except StopIteration:
            pass

        dfs = a1.dfs()

        # first match should be tier2
        self.assertTrue(
            dfs.next() in tier2,
            "First DFS incorrect"
            )

        # second match should be tier3
        self.assertTrue(
            dfs.next() in tier3,
            "Second DFS incorrect"
            )
        # third match should be tier3
        self.assertTrue(
            dfs.next() in tier3,
            "Third DFS incorrect"
            )
        # fourth match should be tier 2
        self.assertTrue(
            dfs.next() in tier2,
            "Fourth DFS incorrect"
            )
        # fifth match should be tier 3
        self.assertTrue(
            dfs.next() in tier3,
            "Fifth DFS incorrect"
            )
        # sixth match should be tier3
        self.assertTrue(
            dfs.next() in tier3,
            "Sixth DFS incorrect"
            )

if __name__ == '__main__':
    unittest.main()

