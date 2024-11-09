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
import sys

from llnl.util import tty
from llnl.util.filesystem import join_path
from llnl.util.lang import memoized

from spack.util.executable import Executable, which


def _ensure_file_on_win():
    """Ensures the file command is available on Windows
    If not, it is bootstrapped.
    No-op on all other platforms"""
    if sys.platform != "win32":
        return
    import spack.bootstrap

    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_file_in_path_or_raise()


@memoized
def file_command(*args):
    """Creates entry point to `file` system command with provided arguments"""
    _ensure_file_on_win()
    file_cmd = which("file", required=True)
    for arg in args:
        file_cmd.add_default_arg(arg)
    return file_cmd


@memoized
def _get_mime_type():
    """Generate method to call `file` system command to aquire mime type
    for a specified path
    """
    if sys.platform == "win32":
        # -h option (no-dereference) does not exist in Windows
        return file_command("-b", "--mime-type")
    else:
        return file_command("-b", "-h", "--mime-type")


def mime_type(filename):
    """Returns the mime type and subtype of a file.

    Args:
        filename: file to be analyzed

    Returns:
        Tuple containing the MIME type and subtype
    """
    output = _get_mime_type()(filename, output=str, error=str).strip()
    tty.debug("==> " + output)
    type, _, subtype = output.partition("/")
    return type, subtype


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
    libs = glob.glob(join_path(path, "*.dylib"))
    for lib in libs:
        # fix install name first:
        install_name_tool = Executable("install_name_tool")
        install_name_tool("-id", lib, lib)
        otool = Executable("otool")
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
                    install_name_tool("-change", dep, loc, lib)
                    break
