# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import stat
import re
import sys

import llnl.util.tty as tty
import llnl.util.filesystem as fs

import spack.modules
import spack.paths
import spack.store


#: Character limit for shebang line.  Using Linux's 127 characters
#: here, as it is the shortest I could find on a modern OS.
shebang_limit = 127


def sbang_install_path():
    """Location sbang should be installed within Spack's ``install_tree``."""
    return os.path.join(spack.store.layout.root, "bin", "sbang")


def sbang_shebang_line():
    """Full shebang line that should be prepended to files to use sbang.

    The line returned does not have a final newline (caller should add it
    if needed).

    This should be the only place in Spack that knows about what
    interpreter we use for ``sbang``.
    """
    return '#!/bin/sh %s' % sbang_install_path()


def shebang_too_long(path):
    """Detects whether a file has a shebang line that is too long."""
    if not os.path.isfile(path):
        return False

    with open(path, 'rb') as script:
        bytes = script.read(2)
        if bytes != b'#!':
            return False

        line = bytes + script.readline()
        return len(line) > shebang_limit


def filter_shebang(path):
    """Adds a second shebang line, using sbang, at the beginning of a file."""
    with open(path, 'rb') as original_file:
        original = original_file.read()
        if sys.version_info >= (2, 7):
            original = original.decode(encoding='UTF-8')
        else:
            original = original.decode('UTF-8')

    # This line will be prepended to file
    new_sbang_line = '%s\n' % sbang_shebang_line()

    # Skip files that are already using sbang.
    if original.startswith(new_sbang_line):
        return

    # In the following, newlines have to be excluded in the regular expression
    # else any mention of "lua" in the document will lead to spurious matches.

    # Use --! instead of #! on second line for lua.
    if re.search(r'^#!(/[^/\n]*)*lua\b', original):
        original = re.sub(r'^#', '--', original)

    # Use <?php #! instead of #! on second line for php.
    if re.search(r'^#!(/[^/\n]*)*php\b', original):
        original = re.sub(r'^#', '<?php #', original) + ' ?>'

    # Use //! instead of #! on second line for node.js.
    if re.search(r'^#!(/[^/\n]*)*node\b', original):
        original = re.sub(r'^#', '//', original)

    # Change non-writable files to be writable if needed.
    saved_mode = None
    if not os.access(path, os.W_OK):
        st = os.stat(path)
        saved_mode = st.st_mode
        os.chmod(path, saved_mode | stat.S_IWRITE)

    with open(path, 'wb') as new_file:
        if sys.version_info >= (2, 7):
            new_file.write(new_sbang_line.encode(encoding='UTF-8'))
            new_file.write(original.encode(encoding='UTF-8'))
        else:
            new_file.write(new_sbang_line.encode('UTF-8'))
            new_file.write(original.encode('UTF-8'))

    # Restore original permissions.
    if saved_mode is not None:
        os.chmod(path, saved_mode)

    tty.debug("Patched overlong shebang in %s" % path)


def filter_shebangs_in_directory(directory, filenames=None):
    if filenames is None:
        filenames = os.listdir(directory)
    for file in filenames:
        path = os.path.join(directory, file)

        # only handle files
        if not os.path.isfile(path):
            continue

        # only handle links that resolve within THIS package's prefix.
        if os.path.islink(path):
            real_path = os.path.realpath(path)
            if not real_path.startswith(directory + os.sep):
                continue

        # test the file for a long shebang, and filter
        if shebang_too_long(path):
            filter_shebang(path)


def install_sbang():
    """Ensure that ``sbang`` is installed in the root of Spack's install_tree.

    This is the shortest known publicly accessible path, and installing
    ``sbang`` here ensures that users can access the script and that
    ``sbang`` itself is in a short path.
    """
    # copy in a new version of sbang if it differs from what's in spack
    sbang_path = sbang_install_path()
    if os.path.exists(sbang_path) and filecmp.cmp(
            spack.paths.sbang_script, sbang_path):
        return

    # make $install_tree/bin and copy in a new version of sbang if needed
    sbang_bin_dir = os.path.dirname(sbang_path)
    fs.mkdirp(sbang_bin_dir)
    fs.install(spack.paths.sbang_script, sbang_path)
    fs.set_install_permissions(sbang_bin_dir)


def post_install(spec):
    """This hook edits scripts so that they call /bin/bash
    $spack_prefix/bin/sbang instead of something longer than the
    shebang limit.
    """
    if spec.external:
        tty.debug('SKIP: shebang filtering [external package]')
        return

    install_sbang()

    for directory, _, filenames in os.walk(spec.prefix):
        filter_shebangs_in_directory(directory, filenames)
