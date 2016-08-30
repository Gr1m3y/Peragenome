# Set default logging handler to avoid "No handler found" warnings.
import logging

SOURCE_URL = 'https://github.com/Gr1m3y/Peragenome'
__version__ = '0.0.1'

def get_version():
    return __version__

# Setup the logger (this is mostly for debugging purposes)
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


print "this just ran"
