# Copyright (c) 2014-2021, Simon Percivall and Spack Project Developers.
#
# SPDX-License-Identifier: Python-2.0

from .unparser import Unparser

__version__ = "1.6.3"


def unparse(tree, py_ver_consistent=False):
    unparser = Unparser(py_ver_consistent=py_ver_consistent)
    return unparser.visit(tree) + "\n"
