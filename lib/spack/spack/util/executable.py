# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import subprocess
import sys
from pathlib import Path, PurePath

import llnl.util.tty as tty

import spack.error
from spack.util.environment import EnvironmentModifications

__all__ = ["Executable", "which", "ProcessError"]


class Executable:
    """Class representing a program that can be run on the command line."""

    def __init__(self, name):
        file_path = str(Path(name))
        if sys.platform != "win32" and name.startswith("."):
            # pathlib strips the ./ from relative paths so it must be added back
            file_path = os.path.join(".", file_path)
        self.exe = [file_path]

        self.default_env = {}

        self.default_envmod = EnvironmentModifications()
        self.returncode = None
        self.ignore_quotes = False

        if not self.exe:
            raise ProcessError("Cannot construct executable for '%s'" % name)

    def add_default_arg(self, *args):
        """Add default argument(s) to the command."""
        self.exe.extend(args)

    def with_default_args(self, *args):
        """Same as add_default_arg, but returns a copy of the executable."""
        new = self.copy()
        new.add_default_arg(*args)
        return new

    def copy(self):
        """Return a copy of this Executable."""
        new = Executable(self.exe[0])
        new.exe[:] = self.exe
        new.default_env.update(self.default_env)
        new.default_envmod.extend(self.default_envmod)
        return new

    def add_default_env(self, key, value):
        """Set an environment variable when the command is run.

        Parameters:
            key: The environment variable to set
            value: The value to set it to
        """
        self.default_env[key] = value

    def add_default_envmod(self, envmod):
        """Set an EnvironmentModifications to use when the command is run."""
        self.default_envmod.extend(envmod)

    @property
    def command(self):
        """The command-line string.

        Returns:
            str: The executable and default arguments
        """
        return " ".join(self.exe)

    @property
    def name(self):
        """The executable name.

        Returns:
            str: The basename of the executable
        """
        return PurePath(self.path).name

    @property
    def path(self):
        """The path to the executable.

        Returns:
            str: The path to the executable
        """
        return str(PurePath(self.exe[0]))

    def __call__(self, *args, **kwargs):
        """Run this executable in a subprocess.

        Parameters:
            *args (str): Command-line arguments to the executable to run

        Keyword Arguments:
            _dump_env (dict): Dict to be set to the environment actually
                used (envisaged for testing purposes only)
            env (dict or EnvironmentModifications): The environment with which
                to run the executable
            extra_env (dict or EnvironmentModifications): Extra items to add to
                the environment (neither requires nor precludes env)
            fail_on_error (bool): Raise an exception if the subprocess returns
                an error. Default is True. The return code is available as
                ``exe.returncode``
            ignore_errors (int or list): A list of error codes to ignore.
                If these codes are returned, this process will not raise
                an exception even if ``fail_on_error`` is set to ``True``
            ignore_quotes (bool): If False, warn users that quotes are not needed
                as Spack does not use a shell. Defaults to False.
            timeout (int or float): The number of seconds to wait before killing
                the child process
            input: Where to read stdin from
            output: Where to send stdout
            error: Where to send stderr

        Accepted values for input, output, and error:

        * python streams, e.g. open Python file objects, or ``os.devnull``
        * filenames, which will be automatically opened for writing
        * ``str``, as in the Python string type. If you set these to ``str``,
          output and error will be written to pipes and returned as a string.
          If both ``output`` and ``error`` are set to ``str``, then one string
          is returned containing output concatenated with error. Not valid
          for ``input``
        * ``str.split``, as in the ``split`` method of the Python string type.
          Behaves the same as ``str``, except that value is also written to
          ``stdout`` or ``stderr``.

        By default, the subprocess inherits the parent's file descriptors.

        """

        def process_cmd_output(out, err):
            result = None
            if output in (str, str.split) or error in (str, str.split):
                result = ""
                if output in (str, str.split):
                    if sys.platform == "win32":
                        outstr = str(out.decode("ISO-8859-1"))
                    else:
                        outstr = str(out.decode("utf-8"))
                    result += outstr
                    if output is str.split:
                        sys.stdout.write(outstr)
                if error in (str, str.split):
                    if sys.platform == "win32":
                        errstr = str(err.decode("ISO-8859-1"))
                    else:
                        errstr = str(err.decode("utf-8"))
                    result += errstr
                    if error is str.split:
                        sys.stderr.write(errstr)
            return result

        # Environment
        env_arg = kwargs.get("env", None)

        # Setup default environment
        env = os.environ.copy() if env_arg is None else {}
        self.default_envmod.apply_modifications(env)
        env.update(self.default_env)

        from spack.util.environment import EnvironmentModifications  # no cycle

        # Apply env argument
        if isinstance(env_arg, EnvironmentModifications):
            env_arg.apply_modifications(env)
        elif env_arg:
            env.update(env_arg)

        # Apply extra env
        extra_env = kwargs.get("extra_env", {})
        if isinstance(extra_env, EnvironmentModifications):
            extra_env.apply_modifications(env)
        else:
            env.update(extra_env)

        if "_dump_env" in kwargs:
            kwargs["_dump_env"].clear()
            kwargs["_dump_env"].update(env)

        fail_on_error = kwargs.pop("fail_on_error", True)
        ignore_errors = kwargs.pop("ignore_errors", ())
        ignore_quotes = kwargs.pop("ignore_quotes", self.ignore_quotes)
        timeout = kwargs.pop("timeout", None)

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        input = kwargs.pop("input", None)
        output = kwargs.pop("output", None)
        error = kwargs.pop("error", None)

        if input is str:
            raise ValueError("Cannot use `str` as input stream.")

        def streamify(arg, mode):
            if isinstance(arg, str):
                return open(arg, mode), True
            elif arg in (str, str.split):
                return subprocess.PIPE, False
            else:
                return arg, False

        ostream, close_ostream = streamify(output, "w")
        estream, close_estream = streamify(error, "w")
        istream, close_istream = streamify(input, "r")

        if not ignore_quotes:
            quoted_args = [arg for arg in args if re.search(r'^".*"$|^\'.*\'$', arg)]
            if quoted_args:
                tty.warn(
                    "Quotes in command arguments can confuse scripts like" " configure.",
                    "The following arguments may cause problems when executed:",
                    str("\n".join(["    " + arg for arg in quoted_args])),
                    "Quotes aren't needed because spack doesn't use a shell. "
                    "Consider removing them.",
                    "If multiple levels of quotation are required, use " "`ignore_quotes=True`.",
                )

        cmd = self.exe + list(args)

        escaped_cmd = ["'%s'" % arg.replace("'", "'\"'\"'") for arg in cmd]
        cmd_line_string = " ".join(escaped_cmd)
        tty.debug(cmd_line_string)

        try:
            proc = subprocess.Popen(
                cmd, stdin=istream, stderr=estream, stdout=ostream, env=env, close_fds=False
            )
            out, err = proc.communicate(timeout=timeout)

            result = process_cmd_output(out, err)
            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                long_msg = cmd_line_string
                if result:
                    # If the output is not captured in the result, it will have
                    # been stored either in the specified files (e.g. if
                    # 'output' specifies a file) or written to the parent's
                    # stdout/stderr (e.g. if 'output' is not specified)
                    long_msg += "\n" + result

                raise ProcessError("Command exited with status %d:" % proc.returncode, long_msg)

            return result

        except OSError as e:
            message = "Command: " + cmd_line_string
            if " " in self.exe[0]:
                message += "\nDid you mean to add a space to the command?"

            raise ProcessError("%s: %s" % (self.exe[0], e.strerror), message)

        except subprocess.CalledProcessError as e:
            if fail_on_error:
                raise ProcessError(
                    str(e),
                    "\nExit status %d when invoking command: %s"
                    % (proc.returncode, cmd_line_string),
                )
        except subprocess.TimeoutExpired as te:
            proc.kill()
            out, err = proc.communicate()
            result = process_cmd_output(out, err)
            long_msg = cmd_line_string + f"\n{result}"
            if fail_on_error:
                raise ProcessTimeoutError(
                    f"\nProcess timed out after {timeout}s. "
                    "We expected the following command to run quickly but it did not, "
                    f"please report this as an issue: {long_msg}",
                    long_message=long_msg,
                ) from te

        finally:
            if close_ostream:
                ostream.close()
            if close_estream:
                estream.close()
            if close_istream:
                istream.close()

    def __eq__(self, other):
        return hasattr(other, "exe") and self.exe == other.exe

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((type(self),) + tuple(self.exe))

    def __repr__(self):
        return "<exe: %s>" % self.exe

    def __str__(self):
        return " ".join(self.exe)


def which_string(*args, **kwargs):
    """Like ``which()``, but return a string instead of an ``Executable``."""
    path = kwargs.get("path", os.environ.get("PATH", ""))
    required = kwargs.get("required", False)

    if isinstance(path, list):
        paths = [Path(str(x)) for x in path]

    if isinstance(path, str):
        paths = [Path(x) for x in path.split(os.pathsep)]

    def get_candidate_items(search_item):
        if sys.platform == "win32" and not search_item.suffix:
            return [search_item.parent / (search_item.name + ext) for ext in [".exe", ".bat"]]

        return [Path(search_item)]

    def add_extra_search_paths(paths):
        with_parents = []
        with_parents.extend(paths)
        if sys.platform == "win32":
            for p in paths:
                if p.name == "bin":
                    with_parents.append(p.parent)
        return with_parents

    for search_item in args:
        search_paths = []
        search_paths.extend(paths)
        if search_item.startswith("."):
            # we do this because pathlib will strip any leading ./
            search_paths.insert(0, Path.cwd())
        search_paths = add_extra_search_paths(search_paths)

        search_item = Path(search_item)
        candidate_items = get_candidate_items(Path(search_item))

        for candidate_item in candidate_items:
            for directory in search_paths:
                exe = directory / candidate_item
                try:
                    if exe.is_file() and os.access(str(exe), os.X_OK):
                        return str(exe)
                except OSError:
                    pass

    if required:
        raise CommandNotFoundError("spack requires '%s'. Make sure it is in your path." % args[0])

    return None


def which(*args, **kwargs):
    """Finds an executable in the path like command-line which.

    If given multiple executables, returns the first one that is found.
    If no executables are found, returns None.

    Parameters:
        *args (str): One or more executables to search for

    Keyword Arguments:
        path (list or str): The path to search. Defaults to ``PATH``
        required (bool): If set to True, raise an error if executable not found

    Returns:
        Executable: The first executable that is found in the path
    """
    exe = which_string(*args, **kwargs)
    return Executable(exe) if exe else None


class ProcessError(spack.error.SpackError):
    """ProcessErrors are raised when Executables exit with an error code."""


class ProcessTimeoutError(ProcessError):
    """ProcessTimeoutErrors are raised when Executable calls with a
    specified timeout exceed that time"""


class CommandNotFoundError(spack.error.SpackError):
    """Raised when ``which()`` can't find a required executable."""
