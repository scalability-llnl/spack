import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType("r"))
parser.add_argument("out", type=argparse.FileType("w"))

args = parser.parse_args()

args.out.write(os.path.expandvars(args.input.read()))
