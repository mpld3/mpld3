"""
Short script which prints the mpld3 version to stdout

This is used within the Javascript build system.
"""
from _mpld3_setup import get_version
print(get_version())
