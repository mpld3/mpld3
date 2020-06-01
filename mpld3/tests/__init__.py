try:
    from . import export
except ModuleNotFoundError as e:
    print("Export module not loaded")
"""
mpld3 tests
"""

# import matplotlib and set the backend to Agg. This needs to be done before
# pyplot is imported: we set it here so that we don't have to set it in any
# of the individual test files.
import matplotlib
matplotlib.use('Agg')
