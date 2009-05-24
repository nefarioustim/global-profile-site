import cPickle, gzip

def save( filename, *objects ):
    """Save objects into a compressed diskfile."""
    fil = gzip.open( filename, "wb" )
    for obj in objects:
        cPickle.dump( obj, fil, protocol = 2 )
    fil.close()

def load( filename ):
    """Reload objects from a compressed diskfile."""
    fil = gzip.open( filename, "rb" )
    while True:
        try:
            yield cPickle.load( fil )
        except EOFError:
            break
    fil.close()