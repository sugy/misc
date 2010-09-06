#!/usr/bin/env python

import time
class Tail( object ):

    def __init__( self, filename ):
        self.f = open( filename, "rU" )
        self.f.seek( 0, 2 )

    def tail( self, wait=0.1 ):
        while True:
            line = self.f.readline()
            if not line:
                time.sleep( wait )
            else:
                yield line

import sys
t = Tail( sys.argv[1] )

try:
    for line in t.tail():
        try:
            sys.stdout.write( line )
        except ValueError:
            pass
except KeyboardInterrupt:
    pass
