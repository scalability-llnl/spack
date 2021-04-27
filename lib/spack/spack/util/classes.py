# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Need this because of spack.util.string
from __future__ import absolute_import
from spack.util.naming import mod_to_class
from llnl.util.lang import memoized, list_modules
import llnl.util.tty as tty

import inspect

__all__ = [
    'list_classes'
]


@memoized
def list_classes(parent_module, mod_path):
    """Given a parent path (e.g., spack.platforms or spack.analyzers),
    use list_modules to derive the module names, and then mod_to_class
    to derive class names. Import the classes and return them in a list
    """
    classes = []

    for name in list_modules(mod_path):
        mod_name = '%s.%s' % (parent_module, name)
        class_name = mod_to_class(name)
        mod = __import__(mod_name, fromlist=[class_name])
        if not hasattr(mod, class_name):
            tty.die('No class %s defined in %s' % (class_name, mod_name))
        cls = getattr(mod, class_name)
        if not inspect.isclass(cls):
            tty.die('%s.%s is not a class' % (mod_name, class_name))

        classes.append(cls)

    return classes
