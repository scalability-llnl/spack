# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import re
import shutil
import stat
import sys
import tempfile

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.error
import spack.package_prefs
import spack.paths
import spack.spec
import spack.store

#: OS-imposed character limit for shebang line: 127 for Linux; 511 for Mac.
#: Different Linux distributions have different limits, but 127 is the
#: smallest among all modern versions.
if sys.platform == "darwin":
    system_shebang_limit = 511
else:
    system_shebang_limit = 127

#: Groupdb does not exist on Windows, prevent imports
#: on supported systems
if sys.platform != "win32":
    import grp

#: Spack itself also limits the shebang line to at most 4KB, which should be plenty.
spack_shebang_limit = 4096

interpreter_regex = re.compile(b"#![ \t]*?([^ \t\0\n]+)")


def sbang_install_path():
    """Location sbang should be installed within Spack's ``install_tree``."""
    sbang_root = str(spack.store.STORE.unpadded_root)
    install_path = os.path.join(sbang_root, "bin", "sbang")
    path_length = len(install_path)
    if path_length > system_shebang_limit:
        msg = (
            "Install tree root is too long. Spack cannot patch shebang lines"
            " when script path length ({0}) exceeds limit ({1}).\n  {2}"
        )
        msg = msg.format(path_length, system_shebang_limit, install_path)
        raise SbangPathError(msg)
    return install_path


def sbang_shebang_line():
    """Full shebang line that should be prepended to files to use sbang.

    The line returned does not have a final newline (caller should add it
    if needed).

    This should be the only place in Spack that knows about what
    interpreter we use for ``sbang``.
    """
    return "#!/bin/sh %s" % sbang_install_path()


def get_interpreter(binary_string):
    # The interpreter may be preceded with ' ' and \t, is itself any byte that
    # follows until the first occurrence of ' ', \t, \0, \n or end of file.
    match = interpreter_regex.match(binary_string)
    return None if match is None else match.group(1)


def filter_shebang(path):
    """
    Adds a second shebang line, using sbang, at the beginning of a file, if necessary.
    Note: Spack imposes a relaxed shebang line limit, meaning that a newline or end of
    file must occur before ``spack_shebang_limit`` bytes. If not, the file is not
    patched.
    """
    with open(path, "rb") as original:
        # If there is no shebang, we shouldn't replace anything.
        old_shebang_line = original.read(2)
        if old_shebang_line != b"#!":
            return False

        # Stop reading after b'\n'. Note that old_shebang_line includes the first b'\n'.
        old_shebang_line += original.readline(spack_shebang_limit - 2)

        # If the shebang line is short, we don't have to do anything.
        if len(old_shebang_line) <= system_shebang_limit:
            return False

        # Whenever we can't find a newline within the maximum number of bytes, we will
        # not attempt to rewrite it. In principle we could still get the interpreter if
        # only the arguments are truncated, but note that for PHP we need the full line
        # since we have to append `?>` to it. Since our shebang limit is already very
        # generous, it's unlikely to happen, and it should be fine to ignore.
        if len(old_shebang_line) == spack_shebang_limit and old_shebang_line[-1] != b"\n":
            return False

        # This line will be prepended to file
        new_sbang_line = (sbang_shebang_line() + "\n").encode("utf-8")

        # Skip files that are already using sbang.
        if old_shebang_line == new_sbang_line:
            return

        interpreter = get_interpreter(old_shebang_line)

        # If there was only whitespace we don't have to do anything.
        if not interpreter:
            return False

        # Store the file permissions, the patched version needs the same.
        saved_mode = os.stat(path).st_mode

        # Change non-writable files to be writable if needed.
        if not os.access(path, os.W_OK):
            os.chmod(path, saved_mode | stat.S_IWUSR)

        # No need to delete since we'll move it and overwrite the original.
        patched = tempfile.NamedTemporaryFile("wb", delete=False)
        patched.write(new_sbang_line)

        # Note that in Python this does not go out of bounds even if interpreter is a
        # short byte array.
        # Note: if the interpreter string was encoded with UTF-16, there would have
        # been a \0 byte between all characters of lua, node, php; meaning that it would
        # lead to truncation of the interpreter. So we don't have to worry about weird
        # encodings here, and just looking at bytes is justified.
        if interpreter[-4:] == b"/lua" or interpreter[-7:] == b"/luajit":
            # Use --! instead of #! on second line for lua.
            patched.write(b"--!" + old_shebang_line[2:])
        elif interpreter[-5:] == b"/node":
            # Use //! instead of #! on second line for node.js.
            patched.write(b"//!" + old_shebang_line[2:])
        elif interpreter[-4:] == b"/php":
            # Use <?php #!... ?> instead of #!... on second line for php.
            patched.write(b"<?php " + old_shebang_line + b" ?>")
        else:
            patched.write(old_shebang_line)

        # After copying the remainder of the file, we can close the original
        shutil.copyfileobj(original, patched)

    # And close the temporary file so we can move it.
    patched.close()

    # Overwrite original file with patched file, and keep the original mode
    shutil.move(patched.name, path)
    os.chmod(path, saved_mode)
    return True


def filter_shebangs_in_directory(directory, filenames=None):
    if filenames is None:
        filenames = os.listdir(directory)

    is_exe = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

    for file in filenames:
        path = os.path.join(directory, file)

        # Only look at executable, non-symlink files.
        try:
            st = os.lstat(path)
        except (IOError, OSError):
            continue

        if stat.S_ISLNK(st.st_mode) or stat.S_ISDIR(st.st_mode) or not st.st_mode & is_exe:
            continue

        # test the file for a long shebang, and filter
        if filter_shebang(path):
            tty.debug("Patched overlong shebang in %s" % path)


def install_sbang():
    """Ensure that ``sbang`` is installed in the root of Spack's install_tree.

    This is the shortest known publicly accessible path, and installing
    ``sbang`` here ensures that users can access the script and that
    ``sbang`` itself is in a short path.
    """
    # copy in a new version of sbang if it differs from what's in spack
    sbang_path = sbang_install_path()
    if os.path.exists(sbang_path) and filecmp.cmp(spack.paths.sbang_script, sbang_path):
        return

    # make $install_tree/bin
    sbang_bin_dir = os.path.dirname(sbang_path)
    fs.mkdirp(sbang_bin_dir)

    # get permissions for bin dir from configuration files
    group_name = spack.package_prefs.get_package_group(spack.spec.Spec("all"))
    config_mode = spack.package_prefs.get_package_dir_permissions(spack.spec.Spec("all"))

    if group_name:
        os.chmod(sbang_bin_dir, config_mode)  # Use package directory permissions
    else:
        fs.set_install_permissions(sbang_bin_dir)

    # set group on sbang_bin_dir if not already set (only if set in configuration)
    # TODO: after we drop python2 support, use shutil.chown to avoid gid lookups that
    # can fail for remote groups
    if group_name and os.stat(sbang_bin_dir).st_gid != grp.getgrnam(group_name).gr_gid:
        os.chown(sbang_bin_dir, os.stat(sbang_bin_dir).st_uid, grp.getgrnam(group_name).gr_gid)

    # copy over the fresh copy of `sbang`
    sbang_tmp_path = os.path.join(
        os.path.dirname(sbang_path), ".%s.tmp" % os.path.basename(sbang_path)
    )
    shutil.copy(spack.paths.sbang_script, sbang_tmp_path)

    # set permissions on `sbang` (including group if set in configuration)
    os.chmod(sbang_tmp_path, config_mode)
    if group_name:
        os.chown(sbang_tmp_path, os.stat(sbang_tmp_path).st_uid, grp.getgrnam(group_name).gr_gid)

    # Finally, move the new `sbang` into place atomically
    os.rename(sbang_tmp_path, sbang_path)


def post_install(spec, explicit=None):
    """This hook edits scripts so that they call /bin/bash
    $spack_prefix/bin/sbang instead of something longer than the
    shebang limit.
    """
    if sys.platform == "win32":
        return
    if spec.external:
        tty.debug("SKIP: shebang filtering [external package]")
        return

    install_sbang()

    for directory, _, filenames in os.walk(spec.prefix):
        filter_shebangs_in_directory(directory, filenames)


class SbangPathError(spack.error.SpackError):
    """Raised when the install tree root is too long for sbang to work."""
