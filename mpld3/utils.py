import os
import warnings
from functools import wraps

# Make sure that DeprecationWarning get printed
warnings.simplefilter("always", DeprecationWarning)


def get_id(obj, suffix=None):
    """Get a unique id for the object"""
    objid = str(os.getpid()) + str(id(obj))
    if suffix:
        objid += str(suffix)
    return objid


def deprecated(func, old_name, new_name):
    """Decorator to mark functions as deprecated."""
    @wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(("{0} is deprecated and will be removed.  "
                       "Use {1} instead".format(old_name, new_name)),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    return new_func
