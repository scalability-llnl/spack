# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Module for finding the user's preferred text editor.

Defines one function, editor(), which invokes the editor defined by the
user's VISUAL environment variable if set. We fall back to the editor
defined by the EDITOR environment variable if VISUAL is not set or the
specified editor fails (e.g. no DISPLAY for a graphical editor). If
neither variable is set, we fall back to one of several common editors,
raising an EnvironmentError if we are unable to find one.
"""
import os
import shlex
from typing import Callable, List

import llnl.util.tty as tty

import spack.config
import spack.util.executable

#: editors to try if VISUAL and EDITOR are not set
_default_editors = ["vim", "vi", "emacs", "nano", "notepad"]


def _find_exe_from_env_var(var: str):
    """Find an executable from an environment variable.

    Args:
        var (str): environment variable name

    Returns:
        (str or None, list): executable string (or None if not found) and
            arguments parsed from the env var
    """
    # try to get the environment variable
    exe = os.environ.get(var)
    if not exe:
        return None, []

    # split env var into executable and args if needed
    args = shlex.split(str(exe))

    if not args:
        return None, []

    exe = spack.util.executable.which_string(args[0])
    args = [exe] + args[1:]
    return exe, args


def executable(exe: str, args: List[str]) -> int:
    """Wrapper that makes ``spack.util.executable.Executable`` look like ``os.execv()``.

    Use this with ``editor()`` if you want it to return instead of running ``execv``.
    """
    cmd = spack.util.executable.Executable(exe)
    cmd(*args[1:], fail_on_error=False)
    return cmd.returncode


def editor(*args: str, exec_fn: Callable[[str, List[str]], int] = os.execv) -> bool:
    """Invoke the user's editor.

    This will try to execute the following, in order:

      1. $VISUAL <args>    # the "visual" editor (per POSIX)
      2. $EDITOR <args>    # the regular editor (per POSIX)
      3. some default editor (see ``_default_editors``) with <args>

    If an environment variable isn't defined, it is skipped.  If it
    points to something that can't be executed, we'll print a
    warning. And if we can't find anything that can be executed after
    searching the full list above, we'll raise an error.

    Arguments:
        args: args to pass to editor

    Optional Arguments:
        exec_fn: invoke this function to run; use ``spack.util.editor.executable`` if you
            want something that returns, instead of the default ``os.execv()``.
    """

    def try_exec(exe, args, var=None):
        """Try to execute an editor with execv, and warn if it fails.

        Returns: (bool) False if the editor failed, ideally does not
            return if ``execv`` succeeds, and ``True`` if the
            ``exec`` does return successfully.
        """
        # gvim runs in the background by default so we force it to run
        # in the foreground to ensure it gets attention.
        if "gvim" in exe and "-f" not in args:
            exe, *rest = args
            args = [exe, "-f"] + rest

        try:
            return exec_fn(exe, args) == 0

        except (OSError, spack.util.executable.ProcessError) as e:
            if spack.config.get("config:debug"):
                raise

            # Show variable we were trying to use, if it's from one
            if var:
                exe = "$%s (%s)" % (var, exe)
            tty.warn("Could not execute %s due to error:" % exe, str(e))
            return False

    def try_env_var(var):
        """Find an editor from an environment variable and try to exec it.

        This will warn if the variable points to something is not
        executable, or if there is an error when trying to exec it.
        """
        if var not in os.environ:
            return False

        exe, editor_args = _find_exe_from_env_var(var)
        if not exe:
            tty.warn("$%s is not an executable:" % var, os.environ[var])
            return False

        full_args = editor_args + list(args)
        return try_exec(exe, full_args, var)

    # try standard environment variables
    if try_env_var("SPACK_EDITOR"):
        return True
    if try_env_var("VISUAL"):
        return True
    if try_env_var("EDITOR"):
        return True

    # nothing worked -- try the first default we can find don't bother
    # trying them all -- if we get here and one fails, something is
    # probably much more deeply wrong with the environment.
    exe = spack.util.executable.which_string(*_default_editors)
    if exe and try_exec(exe, [exe] + list(args)):
        return True

    # Fail if nothing could be found
    raise EnvironmentError(
        "No text editor found! Please set the VISUAL and/or EDITOR "
        "environment variable(s) to your preferred text editor."
    )
