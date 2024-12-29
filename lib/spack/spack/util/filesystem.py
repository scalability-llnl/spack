# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utilities for interacting with files,
like those in llnl.util.filesystem, but which require logic from spack.util
"""

import glob
import os

from llnl.util.filesystem import edit_in_place_through_temporary_file

from spack.util.executable import Executable


def fix_darwin_install_name(path):
    """Fix install name of dynamic libraries on Darwin to have full path.

    There are two parts of this task:

    1. Use ``install_name('-id', ...)`` to change install name of a single lib
    2. Use ``install_name('-change', ...)`` to change the cross linking between
       libs. The function assumes that all libraries are in one folder and
       currently won't follow subfolders.

    Parameters:
        path (str): directory in which .dylib files are located
    """
    libs = glob.glob(os.path.join(path, "*.dylib"))
    install_name_tool = Executable("install_name_tool")
    otool = Executable("otool")
    for lib in libs:
        args = ["-id", lib]
        long_deps = otool("-L", lib, output=str).split("\n")
        deps = [dep.partition(" ")[0][1::] for dep in long_deps[2:-1]]
        # fix all dependencies:
        for dep in deps:
            for loc in libs:
                # We really want to check for either
                #     dep == os.path.basename(loc)   or
                #     dep == join_path(builddir, os.path.basename(loc)),
                # but we don't know builddir (nor how symbolic links look
                # in builddir). We thus only compare the basenames.
                if os.path.basename(dep) == os.path.basename(loc):
                    args.extend(("-change", dep, loc))
                    break

        with edit_in_place_through_temporary_file(lib) as tmp:
            install_name_tool(*args, tmp)
