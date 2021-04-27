# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating analyzers to extract Application
Binary Interface (ABI) information, along with simple analyses that just load
existing metadata.
"""

from __future__ import absolute_import

import spack.util.classes
import spack.paths

import llnl.util.tty as tty


mod_path = spack.paths.analyzers_path
analyzers = spack.util.classes.list_classes("spack.analyzers", mod_path)

# The base analyzer does not have a name, and cannot do dict comprehension
analyzer_types = {}
for a in analyzers:
    if not hasattr(a, "name"):
        continue
    analyzer_types[a.name] = a


def list_all():
    """A helper function to list all analyzers and their descriptions
    """
    for name, analyzer in analyzer_types.items():
        print("%-25s: %-35s" % (name, analyzer.description))


def get_analyzer(name):
    """Courtesy function to retrieve an analyzer, and exit on error if it
    does not exist.
    """
    if name in analyzer_types:
        return analyzer_types[name]
    tty.die("Analyzer %s does not exist" % name)
