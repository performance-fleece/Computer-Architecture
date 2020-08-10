#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) > 2:
    print('too many arguments')

if len(sys.argv) == 1:
    print('please provide a file to load')

if len(sys.argv) == 2:
    cpu = CPU()
    cpu.load()
    cpu.run()
