# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utilities for managing paths in Spack.

TODO: this is really part of spack.config. Consolidate it.
"""
import os
import re
import getpass
import subprocess
import tempfile

import llnl.util.tty as tty
from llnl.util.lang import memoized

import spack.paths
import spack.util.spack_yaml as syaml

__all__ = [
    'substitute_config_variables',
    'substitute_path_variables',
    'canonicalize_path']

# Substitutions to perform
replacements = {
    'spack': spack.paths.prefix,
    'user': getpass.getuser(),
    'tempdir': tempfile.gettempdir(),
}

# This is intended to be longer than the part of the install path
# spack generates from the root path we give it.  Included in the
# estimate:
#
#   os-arch      ->   30
#   compiler     ->   30
#   package name ->   50   (longest is currently 47 characters)
#   version      ->   20
#   hash         ->   32
#   buffer       ->  138
#  ---------------------
#   total        ->  300
SPACK_MAX_INSTALL_PATH_LENGTH = 300
SPACK_PATH_PADDING_CHARS = 'spack_path_placeholder'


@memoized
def get_system_path_max():
    # Choose a conservative default
    sys_max_path_length = 256
    try:
        path_max_proc  = subprocess.Popen(['getconf', 'PATH_MAX', '/'],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT)
        proc_output = str(path_max_proc.communicate()[0].decode())
        sys_max_path_length = int(proc_output)
    except (ValueError, subprocess.CalledProcessError, OSError):
        tty.msg('Unable to find system max path length, using: {0}'.format(
            sys_max_path_length))

    return sys_max_path_length


def substitute_config_variables(path):
    """Substitute placeholders into paths.

    Spack allows paths in configs to have some placeholders, as follows:

    - $spack     The Spack instance's prefix
    - $user      The current user's username
    - $tempdir   Default temporary directory returned by tempfile.gettempdir()
    - $env       The active Spack environment.

    These are substituted case-insensitively into the path, and users can
    use either ``$var`` or ``${var}`` syntax for the variables. $env is only
    replaced if there is an active environment, and should only be used in
    environment yaml files.
    """
    import spack.environment as ev  # break circular
    env = ev.get_env({}, '')
    if env:
        replacements.update({'env': env.path})
    else:
        # If a previous invocation added env, remove it
        replacements.pop('env', None)

    # Look up replacements
    def repl(match):
        m = match.group(0).strip('${}')
        return replacements.get(m.lower(), match.group(0))

    # Replace $var or ${var}.
    return re.sub(r'(\$\w+\b|\$\{\w+\})', repl, path)


def substitute_path_variables(path):
    """Substitute config vars, expand environment vars, expand user home."""
    path = substitute_config_variables(path)
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    return path


def _get_padding_string(length):
    spack_path_padding_size = len(SPACK_PATH_PADDING_CHARS)
    num_reps = int(length / (spack_path_padding_size + 1))
    extra_chars = length % (spack_path_padding_size + 1)
    reps_list = [SPACK_PATH_PADDING_CHARS for i in range(num_reps)]
    reps_list.append(SPACK_PATH_PADDING_CHARS[:extra_chars])
    return os.path.sep.join(reps_list)


def add_padding(path, length):
    """Add padding subdirectories to path until total is length characters

    Returns the padded path. If path is length - 1 or more characters long,
    returns path. If path is length - 1 characters, warns that it is not
    padding to length

    Assumes path does not have a trailing path separator"""
    padding_length = length - len(path)
    if padding_length == 1:
        # The only 1 character addition we can make to a path is `/`
        # Spack internally runs normpath, so `foo/` will be reduced to `foo`
        # Even if we removed this behavior from Spack, the user could normalize
        # the path, removing the additional `/`.
        # Because we can't expect one character of padding to show up in the
        # resulting binaries, we warn the user and do not pad by a single char
        tty.warn("Cannot pad path by exactly one character.")
    if padding_length <= 0:
        return path

    # we subtract 1 from the padding_length to account for the path separator
    # coming from os.path.join below
    padding = _get_padding_string(padding_length - 1)

    return os.path.join(path, padding)


def canonicalize_path(path):
    """Same as substitute_path_variables, but also take absolute path."""
    # Get file in which path was written in case we need to make it absolute
    # relative to that path.
    filename = None
    if isinstance(path, syaml.syaml_str):
        filename = os.path.dirname(path._start_mark.name)
        assert path._start_mark.name == path._end_mark.name

    path = substitute_path_variables(path)
    if not os.path.isabs(path):
        if filename:
            path = os.path.join(filename, path)
        else:
            path = os.path.abspath(path)
            tty.debug("Using current working directory as base for abspath")

    return os.path.normpath(path)
