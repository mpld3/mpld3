"""
Quick script to output JS code for including the listed icons in base64

Usage: python base64_conv.py <filenames>
"""
import os
import argparse
import json


def compute_base64_encoding(filename):
    base, suffix = os.path.splitext(filename)
    suffix = suffix.lstrip('.')

    with open(filename, 'rb') as f:
        data = f.read().encode("base64")
    
    return (base, "data:image/{0};base64,{1}".format(suffix, data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs='*', type=str)
    args = parser.parse_args()

    encodings = dict([compute_base64_encoding(filename)
                      for filename in args.files])

    print json.dumps(dict(encodings))

if __name__ == "__main__":
    main()
    
    
