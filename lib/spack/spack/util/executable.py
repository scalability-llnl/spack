# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import subprocess
import sys
from pathlib import Path, PurePath
from typing import Callable, Dict, Optional, Sequence, TextIO, Type, Union, overload

import llnl.util.tty as tty

import spack.error
from spack.util.environment import EnvironmentModifications

__all__ = ["Executable", "which", "which_string", "ProcessError"]


class Executable:
    """Class representing a program that can be run on the command line."""

    def __init__(self, name: str) -> None:
        file_path = str(Path(name))
        if sys.platform != "win32" and name.startswith("."):
            # pathlib strips the ./ from relative paths so it must be added back
            file_path = os.path.join(".", file_path)

        self.exe = [file_path]
        self.default_env: Dict[str, str] = {}
        self.default_envmod = EnvironmentModifications()
        self.returncode = 0
        self.ignore_quotes = False

    def add_default_arg(self, *args: str) -> None:
        """Add default argument(s) to the command."""
        self.exe.extend(args)

    def with_default_args(self, *args: str) -> "Executable":
        """Same as add_default_arg, but returns a copy of the executable."""
        new = self.copy()
        new.add_default_arg(*args)
        return new

    def copy(self) -> "Executable":
        """Return a copy of this Executable."""
        new = Executable(self.exe[0])
        new.exe[:] = self.exe
        new.default_env.update(self.default_env)
        new.default_envmod.extend(self.default_envmod)
        return new

    def add_default_env(self, key: str, value: str) -> None:
        """Set an environment variable when the command is run.

        Parameters:
            key: The environment variable to set
            value: The value to set it to
        """
        self.default_env[key] = value

    def add_default_envmod(self, envmod: EnvironmentModifications) -> None:
        """Set an EnvironmentModifications to use when the command is run."""
        self.default_envmod.extend(envmod)

    @property
    def command(self) -> str:
        """Returns the entire command-line string"""
        return " ".join(self.exe)

    @property
    def name(self) -> str:
        """Returns the executable name"""
        return PurePath(self.path).name

    @property
    def path(self) -> str:
        """Returns the executable path"""
        return str(PurePath(self.exe[0]))

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Optional[TextIO], str] = ...,
        error: Union[Optional[TextIO], str] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> None: ...

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Type[str], Callable],
        error: Union[Optional[TextIO], str, Type[str], Callable] = ...,
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    @overload
    def __call__(
        self,
        *args: str,
        fail_on_error: bool = ...,
        ignore_errors: Union[int, Sequence[int]] = ...,
        ignore_quotes: Optional[bool] = ...,
        timeout: Optional[int] = ...,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = ...,
        input: Optional[TextIO] = ...,
        output: Union[Optional[TextIO], str, Type[str], Callable] = ...,
        error: Union[Type[str], Callable],
        _dump_env: Optional[Dict[str, str]] = ...,
    ) -> str: ...

    def __call__(
        self,
        *args: str,
        fail_on_error: bool = True,
        ignore_errors: Union[int, Sequence[int]] = (),
        ignore_quotes: Optional[bool] = None,
        timeout: Optional[int] = None,
        env: Optional[Union[Dict[str, str], EnvironmentModifications]] = None,
        extra_env: Optional[Union[Dict[str, str], EnvironmentModifications]] = None,
        input: Optional[TextIO] = None,
        output: Union[Optional[TextIO], str, Type[str], Callable] = None,
        error: Union[Optional[TextIO], str, Type[str], Callable] = None,
        _dump_env: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        """Runs this executable in a subprocess.

        Parameters:
            *args: command-line arguments to the executable to run
            fail_on_error: if True, raises an exception if the subprocess returns an error
                The return code is available as ``self.returncode``
            ignore_errors: a sequence of error codes to ignore. If these codes are returned, this
                process will not raise an exception, even if ``fail_on_error`` is set to ``True``
            ignore_quotes: if False, warn users that quotes are not needed, as Spack does not
                use a shell. If None, use ``self.ignore_quotes``.
            timeout: the number of seconds to wait before killing the child process
            env: the environment with which to run the executable
            extra_env: extra items to add to the environment (neither requires nor precludes env)
            input: where to read stdin from
            output: where to send stdout
            error: where to send stderr
            _dump_env: dict to be set to the environment actually used (envisaged for
                testing purposes only)

        Accepted values for input, output, and error:

        * python streams, e.g. open Python file objects, or ``os.devnull``
        * ``str``, as in the Python string type. If you set these to ``str``,
          output and error will be written to pipes and returned as a string.
          If both ``output`` and ``error`` are set to ``str``, then one string
          is returned containing output concatenated with error. Not valid
          for ``input``
        * ``str.split``, as in the ``split`` method of the Python string type.
          Behaves the same as ``str``, except that value is also written to
          ``stdout`` or ``stderr``.

        For output and error it's also accepted:

        * filenames, which will be automatically opened for writing

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

        # Setup default environment
        current_environment = os.environ.copy() if env is None else {}
        self.default_envmod.apply_modifications(current_environment)
        current_environment.update(self.default_env)

        # Apply env argument
        if isinstance(env, EnvironmentModifications):
            env.apply_modifications(current_environment)
        elif env:
            current_environment.update(env)

        # Apply extra env
        if isinstance(extra_env, EnvironmentModifications):
            extra_env.apply_modifications(current_environment)
        elif extra_env is not None:
            current_environment.update(extra_env)

        if _dump_env is not None:
            _dump_env.clear()
            _dump_env.update(current_environment)

        if ignore_quotes is None:
            ignore_quotes = self.ignore_quotes

        # If they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        if input is str:
            raise ValueError("Cannot use `str` as input stream.")

        def streamify(arg, mode):
            if isinstance(arg, str):
                return open(arg, mode), True  # pylint: disable=unspecified-encoding
            elif arg in (str, str.split):
                return subprocess.PIPE, False
            else:
                return arg, False

        ostream, close_ostream = streamify(output, "wb")
        estream, close_estream = streamify(error, "wb")
        istream, close_istream = streamify(input, "rb")

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

        result = None
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=istream,
                stderr=estream,
                stdout=ostream,
                env=current_environment,
                close_fds=False,
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

        return result

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
