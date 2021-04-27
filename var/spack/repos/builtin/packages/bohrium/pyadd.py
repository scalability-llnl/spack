#!/usr/bin/env python
import bohrium as bh


a = bh.array([1, 2, 3])
b = bh.array([3, 4, 5])
c = a + b

if bh.all(c == bh.array([4, 6, 8])):
    print("Success!")
else:
    print("Failure, values not as expected.")
