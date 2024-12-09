# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Set, unset or modify environment variables."""
import collections
import contextlib
import inspect
import json
import os
import os.path
import pickle
import re
import shlex
import subprocess
import sys
from functools import wraps
from typing import Any, Callable, Dict, Iterable, List, MutableMapping, Optional, Tuple, Union

from llnl.path import path_to_os_path, system_path_filter
from llnl.util import tty
from llnl.util.lang import dedupe

if sys.platform == "win32":
    SYSTEM_PATHS = [
        "C:\\",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\Users",
        "C:\\ProgramData",
    ]
    SUFFIXES = []
else:
    SYSTEM_PATHS = ["/", "/usr", "/usr/local"]
    SUFFIXES = ["bin", "bin64", "include", "lib", "lib64"]

SYSTEM_DIRS = [os.path.join(p, s) for s in SUFFIXES for p in SYSTEM_PATHS] + SYSTEM_PATHS

#: used in the compiler wrapper's `/usr/lib|/usr/lib64|...)` case entry
SYSTEM_DIR_CASE_ENTRY = "|".join(sorted(f'"{d}{suff}"' for d in SYSTEM_DIRS for suff in ("", "/")))

_SHELL_SET_STRINGS = {
    "sh": "export {0}={1};\n",
    "csh": "setenv {0} {1};\n",
    "fish": "set -gx {0} {1};\n",
    "bat": 'set "{0}={1}"\n',
    "pwsh": "$Env:{0}='{1}'\n",
}


_SHELL_UNSET_STRINGS = {
    "sh": "unset {0};\n",
    "csh": "unsetenv {0};\n",
    "fish": "set -e {0};\n",
    "bat": 'set "{0}="\n',
    "pwsh": "Set-Item -Path Env:{0}\n",
}


TRACING_ENABLED = False

Path = str
ModificationList = List[Union["NameModifier", "NameValueModifier"]]


def system_env_normalize(func):
    """Decorator wrapping calls to system env modifications,
    converting all env variable names to all upper case on Windows, no-op
    on other platforms before calling env modification method.

    Windows, due to a DOS holdover, treats all env variable names case
    insensitively, however Spack's env modification class does not,
    meaning setting `Path` and `PATH` would be distinct env operations
    for Spack, but would cause a collision when actually performing the
    env modification operations on the env.
    Normalize all env names to all caps to prevent this collision from the
    Spack side."""

    @wraps(func)
    def case_insensitive_modification(self, name: str, *args, **kwargs):
        if sys.platform == "win32":
            name = name.upper()
        return func(self, name, *args, **kwargs)

    return case_insensitive_modification


def is_system_path(path: Path) -> bool:
    """Returns True if the argument is a system path, False otherwise."""
    return bool(path) and (os.path.normpath(path) in SYSTEM_DIRS)


def filter_system_paths(paths: Iterable[Path]) -> List[Path]:
    """Returns a copy of the input where system paths are filtered out."""
    return [p for p in paths if not is_system_path(p)]


def deprioritize_system_paths(paths: List[Path]) -> List[Path]:
    """Reorders input paths by putting system paths at the end of the list, otherwise
    preserving order.
    """
    return list(sorted(paths, key=is_system_path))


def prune_duplicate_paths(paths: List[Path]) -> List[Path]:
    """Returns the input list with duplicates removed, otherwise preserving order."""
    return list(dedupe(paths))


def get_path(name: str) -> List[Path]:
    """Given the name of an environment variable containing multiple
    paths separated by 'os.pathsep', returns a list of the paths.
    """
    path = os.environ.get(name, "").strip()
    if path:
        return path.split(os.pathsep)
    return []


def env_flag(name: str) -> bool:
    """Given the name of an environment variable, returns True if it is set to
    'true' or to '1', False otherwise.
    """
    if name in os.environ:
        value = os.environ[name].lower()
        return value in ("true", "1")
    return False


def path_set(var_name: str, directories: List[Path]):
    """Sets the variable passed as input to the `os.pathsep` joined list of directories."""
    path_str = os.pathsep.join(str(dir) for dir in directories)
    os.environ[var_name] = path_str


def path_put_first(var_name: str, directories: List[Path]):
    """Puts the provided directories first in the path, adding them
    if they're not already there.
    """
    path = os.environ.get(var_name, "").split(os.pathsep)

    for directory in directories:
        if directory in path:
            path.remove(directory)

    new_path = list(directories) + list(path)
    path_set(var_name, new_path)


BASH_FUNCTION_FINDER = re.compile(r"BASH_FUNC_(.*?)\(\)")


def _win_env_var_to_set_line(var: str, val: str) -> str:
    is_pwsh = os.environ.get("SPACK_SHELL", None) == "pwsh"
    env_set_phrase = f"$Env:{var}={val}" if is_pwsh else f'set "{var}={val}"'
    return env_set_phrase


def _nix_env_var_to_source_line(var: str, val: str) -> str:
    if var.startswith("BASH_FUNC"):
        source_line = "function {fname}{decl}; export -f {fname}".format(
            fname=BASH_FUNCTION_FINDER.sub(r"\1", var), decl=val
        )
    else:
        source_line = f"{var}={shlex.quote(val)}; export {var}"
    return source_line


def _env_var_to_source_line(var: str, val: str) -> str:
    if sys.platform == "win32":
        return _win_env_var_to_set_line(var, val)
    else:
        return _nix_env_var_to_source_line(var, val)


@system_path_filter(arg_slice=slice(1))
def dump_environment(path: Path, environment: Optional[MutableMapping[str, str]] = None):
    """Dump an environment dictionary to a source-able file.

    Args:
        path: path of the file to write
        environment: environment to be writte. If None os.environ is used.
    """
    use_env = environment or os.environ
    hidden_vars = {"PS1", "PWD", "OLDPWD", "TERM_SESSION_ID"}

    file_descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(file_descriptor, "w") as env_file:
        for var, val in sorted(use_env.items()):
            env_file.write(
                "".join(
                    ["#" if var in hidden_vars else "", _env_var_to_source_line(var, val), "\n"]
                )
            )


@system_path_filter(arg_slice=slice(1))
def pickle_environment(path: Path, environment: Optional[Dict[str, str]] = None):
    """Pickle an environment dictionary to a file."""
    with open(path, "wb") as pickle_file:
        pickle.dump(dict(environment if environment else os.environ), pickle_file, protocol=2)


@contextlib.contextmanager
def set_env(**kwargs):
    """Temporarily sets and restores environment variables.

    Variables can be set as keyword arguments to this function.
    """
    saved = {}
    for var, value in kwargs.items():
        if var in os.environ:
            saved[var] = os.environ[var]

        if value is None:
            if var in os.environ:
                del os.environ[var]
        else:
            os.environ[var] = value

    yield

    for var, value in kwargs.items():
        if var in saved:
            os.environ[var] = saved[var]
        else:
            if var in os.environ:
                del os.environ[var]


class Trace:
    """Trace information on a function call"""

    __slots__ = ("filename", "lineno", "context")

    def __init__(self, *, filename: str, lineno: int, context: str):
        self.filename = filename
        self.lineno = lineno
        self.context = context

    def __str__(self):
        return f"{self.context} at {self.filename}:{self.lineno}"

    def __repr__(self):
        return f"Trace(filename={self.filename}, lineno={self.lineno}, context={self.context})"


class NameModifier:
    """Base class for modifiers that act on the environment variable as a whole, and thus
    store just its name
    """

    __slots__ = ("name", "separator", "trace")

    def __init__(self, name: str, *, separator: str = os.pathsep, trace: Optional[Trace] = None):
        self.name = name
        self.separator = separator
        self.trace = trace

    def __eq__(self, other: object):
        if not isinstance(other, NameModifier):
            return NotImplemented
        return self.name == other.name

    def execute(self, env: MutableMapping[str, str]):
        """Apply the modification to the mapping passed as input"""
        raise NotImplementedError("must be implemented by derived classes")


class NameValueModifier:
    """Base class for modifiers that modify the value of an environment variable."""

    __slots__ = ("name", "value", "separator", "trace")

    def __init__(
        self, name: str, value: Any, *, separator: str = os.pathsep, trace: Optional[Trace] = None
    ):
        self.name = name
        self.value = value
        self.separator = separator
        self.trace = trace

    def __eq__(self, other: object):
        if not isinstance(other, NameValueModifier):
            return NotImplemented
        return (
            self.name == other.name
            and self.value == other.value
            and self.separator == other.separator
        )

    def execute(self, env: MutableMapping[str, str]):
        """Apply the modification to the mapping passed as input"""
        raise NotImplementedError("must be implemented by derived classes")


class SetEnv(NameValueModifier):
    __slots__ = ("force", "raw")

    def __init__(
        self,
        name: str,
        value: str,
        *,
        trace: Optional[Trace] = None,
        force: bool = False,
        raw: bool = False,
    ):
        super().__init__(name, value, trace=trace)
        self.force = force
        self.raw = raw

    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"SetEnv: {self.name}={str(self.value)}", level=3)
        env[self.name] = str(self.value)


class AppendFlagsEnv(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"AppendFlagsEnv: {self.name}={str(self.value)}", level=3)
        if self.name in env and env[self.name]:
            env[self.name] += self.separator + str(self.value)
        else:
            env[self.name] = str(self.value)


class UnsetEnv(NameModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"UnsetEnv: {self.name}", level=3)
        # Avoid throwing if the variable was not set
        env.pop(self.name, None)


class RemoveFlagsEnv(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"RemoveFlagsEnv: {self.name}-{str(self.value)}", level=3)
        environment_value = env.get(self.name, "")
        flags = environment_value.split(self.separator) if environment_value else []
        flags = [f for f in flags if f != self.value]
        env[self.name] = self.separator.join(flags)


class SetPath(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        string_path = self.separator.join(str(item) for item in self.value)
        tty.debug(f"SetPath: {self.name}={string_path}", level=3)
        env[self.name] = string_path


class AppendPath(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"AppendPath: {self.name}+{str(self.value)}", level=3)
        environment_value = env.get(self.name, "")
        directories = environment_value.split(self.separator) if environment_value else []
        directories.append(path_to_os_path(os.path.normpath(self.value)).pop())
        env[self.name] = self.separator.join(directories)


class PrependPath(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"PrependPath: {self.name}+{str(self.value)}", level=3)
        environment_value = env.get(self.name, "")
        directories = environment_value.split(self.separator) if environment_value else []
        directories = [path_to_os_path(os.path.normpath(self.value)).pop()] + directories
        env[self.name] = self.separator.join(directories)


class RemovePath(NameValueModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"RemovePath: {self.name}-{str(self.value)}", level=3)
        environment_value = env.get(self.name, "")
        directories = environment_value.split(self.separator)
        directories = [
            path_to_os_path(os.path.normpath(x)).pop()
            for x in directories
            if x != path_to_os_path(os.path.normpath(self.value)).pop()
        ]
        env[self.name] = self.separator.join(directories)


class DeprioritizeSystemPaths(NameModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"DeprioritizeSystemPaths: {self.name}", level=3)
        environment_value = env.get(self.name, "")
        directories = environment_value.split(self.separator) if environment_value else []
        directories = deprioritize_system_paths(
            [path_to_os_path(os.path.normpath(x)).pop() for x in directories]
        )
        env[self.name] = self.separator.join(directories)


class PruneDuplicatePaths(NameModifier):
    def execute(self, env: MutableMapping[str, str]):
        tty.debug(f"PruneDuplicatePaths: {self.name}", level=3)
        environment_value = env.get(self.name, "")
        directories = environment_value.split(self.separator) if environment_value else []
        directories = prune_duplicate_paths(
            [path_to_os_path(os.path.normpath(x)).pop() for x in directories]
        )
        env[self.name] = self.separator.join(directories)


class EnvironmentModifications:
    """Keeps track of requests to modify the current environment."""

    def __init__(
        self, other: Optional["EnvironmentModifications"] = None, traced: Union[None, bool] = None
    ):
        """Initializes a new instance, copying commands from 'other'
        if it is not None.

        Args:
            other: list of environment modifications to be extended (optional)
            traced: enable or disable stack trace inspection to log the origin
                of the environment modifications
        """
        self.traced = TRACING_ENABLED if traced is None else bool(traced)
        self.env_modifications: List[Union[NameModifier, NameValueModifier]] = []
        if other is not None:
            self.extend(other)

    def __iter__(self):
        return iter(self.env_modifications)

    def __len__(self):
        return len(self.env_modifications)

    def extend(self, other: "EnvironmentModifications"):
        self._check_other(other)
        self.env_modifications.extend(other.env_modifications)

    @staticmethod
    def _check_other(other: "EnvironmentModifications"):
        if not isinstance(other, EnvironmentModifications):
            raise TypeError("other must be an instance of EnvironmentModifications")

    def _trace(self) -> Optional[Trace]:
        """Returns a trace object if tracing is enabled, else None."""
        if not self.traced:
            return None

        stack = inspect.stack()
        try:
            _, filename, lineno, _, context, index = stack[2]
            assert index is not None, "index must be an integer"
            current_context = context[index].strip() if context is not None else "unknown context"
        except Exception:
            filename = "unknown file"
            lineno = -1
            current_context = "unknown context"

        return Trace(filename=filename, lineno=lineno, context=current_context)

    @system_env_normalize
    def set(self, name: str, value: str, *, force: bool = False, raw: bool = False):
        """Stores a request to set an environment variable.

        Args:
            name: name of the environment variable
            value: value of the environment variable
            force: if True, audit will not consider this modification a warning
            raw: if True, format of value string is skipped
        """
        item = SetEnv(name, value, trace=self._trace(), force=force, raw=raw)
        self.env_modifications.append(item)

    @system_env_normalize
    def append_flags(self, name: str, value: str, sep: str = " "):
        """Stores a request to append 'flags' to an environment variable.

        Args:
            name: name of the environment variable
            value: flags to be appended
            sep: separator for the flags (default: " ")
        """
        item = AppendFlagsEnv(name, value, separator=sep, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def unset(self, name: str):
        """Stores a request to unset an environment variable.

        Args:
            name: name of the environment variable
        """
        item = UnsetEnv(name, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def remove_flags(self, name: str, value: str, sep: str = " "):
        """Stores a request to remove flags from an environment variable

        Args:
            name: name of the environment variable
            value: flags to be removed
            sep: separator for the flags (default: " ")
        """
        item = RemoveFlagsEnv(name, value, separator=sep, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def set_path(self, name: str, elements: List[str], separator: str = os.pathsep):
        """Stores a request to set an environment variable to a list of paths,
        separated by a character defined in input.

        Args:
            name: name of the environment variable
            elements: ordered list paths
            separator: separator for the paths (default: os.pathsep)
        """
        item = SetPath(name, elements, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def append_path(self, name: str, path: str, separator: str = os.pathsep):
        """Stores a request to append a path to list of paths.

        Args:
            name: name of the environment variable
            path: path to be appended
            separator: separator for the paths (default: os.pathsep)
        """
        item = AppendPath(name, path, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def prepend_path(self, name: str, path: str, separator: str = os.pathsep):
        """Stores a request to prepend a path to list of paths.

        Args:
            name: name of the environment variable
            path: path to be prepended
            separator: separator for the paths (default: os.pathsep)
        """
        item = PrependPath(name, path, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def remove_path(self, name: str, path: str, separator: str = os.pathsep):
        """Stores a request to remove a path from a list of paths.

        Args:
            name: name of the environment variable
            path: path to be removed
            separator: separator for the paths (default: os.pathsep)
        """
        item = RemovePath(name, path, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def deprioritize_system_paths(self, name: str, separator: str = os.pathsep):
        """Stores a request to deprioritize system paths in a path list,
        otherwise preserving the order.

        Args:
            name: name of the environment variable
            separator: separator for the paths (default: os.pathsep)
        """
        item = DeprioritizeSystemPaths(name, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    @system_env_normalize
    def prune_duplicate_paths(self, name: str, separator: str = os.pathsep):
        """Stores a request to remove duplicates from a path list, otherwise
        preserving the order.

        Args:
            name: name of the environment variable
            separator: separator for the paths (default: os.pathsep)
        """
        item = PruneDuplicatePaths(name, separator=separator, trace=self._trace())
        self.env_modifications.append(item)

    def group_by_name(self) -> Dict[str, ModificationList]:
        """Returns a dict of the current modifications keyed by variable name."""
        modifications = collections.defaultdict(list)
        for item in self:
            modifications[item.name].append(item)
        return modifications

    def drop(self, *name) -> bool:
        """Drop all modifications to the variable with the given name."""
        old_mods = self.env_modifications
        new_mods = [x for x in self.env_modifications if x.name not in name]
        self.env_modifications = new_mods

        return len(old_mods) != len(new_mods)

    def is_unset(self, variable_name: str) -> bool:
        """Returns True if the last modification to a variable is to unset it, False otherwise."""
        modifications = self.group_by_name()
        if variable_name not in modifications:
            return False

        # The last modification must unset the variable for it to be considered unset
        return isinstance(modifications[variable_name][-1], UnsetEnv)

    def clear(self):
        """Clears the current list of modifications."""
        self.env_modifications = []

    def reversed(self) -> "EnvironmentModifications":
        """Returns the EnvironmentModifications object that will reverse self

        Only creates reversals for additions to the environment, as reversing
        ``unset`` and ``remove_path`` modifications is impossible.

        Reversable operations are set(), prepend_path(), append_path(),
        set_path(), and append_flags().
        """
        rev = EnvironmentModifications()

        for envmod in reversed(self.env_modifications):
            if isinstance(envmod, SetEnv):
                tty.debug("Reversing `Set` environment operation may lose the original value")
                rev.unset(envmod.name)
            elif isinstance(envmod, AppendPath):
                rev.remove_path(envmod.name, envmod.value)
            elif isinstance(envmod, PrependPath):
                rev.remove_path(envmod.name, envmod.value)
            elif isinstance(envmod, SetPath):
                tty.debug("Reversing `SetPath` environment operation may lose the original value")
                rev.unset(envmod.name)
            elif isinstance(envmod, AppendFlagsEnv):
                rev.remove_flags(envmod.name, envmod.value)
            else:
                tty.debug(
                    f"Skipping reversal of irreversible operation {type(envmod)} {envmod.name}"
                )

        return rev

    def apply_modifications(self, env: Optional[MutableMapping[str, str]] = None):
        """Applies the modifications and clears the list.

        Args:
            env: environment to be modified. If None, os.environ will be used.
        """
        env = os.environ if env is None else env

        modifications = self.group_by_name()
        for _, actions in sorted(modifications.items()):
            for modifier in actions:
                modifier.execute(env)

    def shell_modifications(
        self,
        shell: str = "sh" if sys.platform != "win32" else os.environ.get("SPACK_SHELL", "bat"),
        explicit: bool = False,
        env: Optional[MutableMapping[str, str]] = None,
    ) -> str:
        """Return shell code to apply the modifications and clears the list."""
        modifications = self.group_by_name()

        env = os.environ if env is None else env
        new_env = dict(env.items())

        for _, actions in sorted(modifications.items()):
            for modifier in actions:
                modifier.execute(new_env)

        if "MANPATH" in new_env and not new_env["MANPATH"].endswith(os.pathsep):
            new_env["MANPATH"] += os.pathsep

        cmds = ""

        for name in sorted(set(modifications)):
            new = new_env.get(name, None)
            old = env.get(name, None)
            if explicit or new != old:
                if new is None:
                    cmds += _SHELL_UNSET_STRINGS[shell].format(name)
                else:
                    value = new_env[name]
                    if shell not in ("bat", "pwsh"):
                        value = shlex.quote(value)
                    cmd = _SHELL_SET_STRINGS[shell].format(name, value)
                    cmds += cmd
        return cmds

    @staticmethod
    def from_sourcing_file(
        filename: Path, *arguments: str, **kwargs: Any
    ) -> "EnvironmentModifications":
        """Returns the environment modifications that have the same effect as
        sourcing the input file.

        Args:
            filename: the file to be sourced
            *arguments: arguments to pass on the command line

        Keyword Args:
            shell (str): the shell to use (default: ``bash``)
            shell_options (str): options passed to the shell (default: ``-c``)
            source_command (str): the command to run (default: ``source``)
            suppress_output (str): redirect used to suppress output of command
                (default: ``&> /dev/null``)
            concatenate_on_success (str): operator used to execute a command
                only when the previous command succeeds (default: ``&&``)
            exclude ([str or re.Pattern[str]]): ignore any modifications of these
                variables (default: [])
            include ([str or re.Pattern[str]]): always respect modifications of these
                variables (default: []). Supersedes any excluded variables.
            clean (bool): in addition to removing empty entries,
                also remove duplicate entries (default: False).
        """
        tty.debug(f"EnvironmentModifications.from_sourcing_file: {filename}")
        # Check if the file actually exists
        if not os.path.isfile(filename):
            msg = f"Trying to source non-existing file: {filename}"
            raise RuntimeError(msg)

        # Prepare include and exclude lists of environment variable names
        exclude = kwargs.get("exclude", [])
        include = kwargs.get("include", [])
        clean = kwargs.get("clean", False)

        # Other variables unrelated to sourcing a file
        exclude.extend(
            [
                # Bash internals
                "SHLVL",
                "_",
                "PWD",
                "OLDPWD",
                "PS1",
                "PS2",
                "ENV",
                # Environment Modules or Lmod
                "LOADEDMODULES",
                "_LMFILES_",
                "MODULEPATH",
                "MODULERCFILE",
                "BASH_FUNC_ml()",
                "BASH_FUNC_module()",
                # Environment Modules-specific configuration
                "MODULESHOME",
                "BASH_FUNC__module_raw()",
                r"MODULES_(.*)",
                r"__MODULES_(.*)",
                r"(\w*)_mod(quar|share)",
                # Lmod-specific configuration
                r"LMOD_(.*)",
            ]
        )

        # Compute the environments before and after sourcing
        before = sanitize(
            environment_after_sourcing_files(os.devnull, **kwargs),
            exclude=exclude,
            include=include,
        )
        file_and_args = (filename,) + arguments
        after = sanitize(
            environment_after_sourcing_files(file_and_args, **kwargs),
            exclude=exclude,
            include=include,
        )

        # Delegate to the other factory
        return EnvironmentModifications.from_environment_diff(before, after, clean)

    @staticmethod
    def from_environment_diff(
        before: MutableMapping[str, str], after: MutableMapping[str, str], clean: bool = False
    ) -> "EnvironmentModifications":
        """Constructs the environment modifications from the diff of two environments.

        Args:
            before: environment before the modifications are applied
            after: environment after the modifications are applied
            clean: in addition to removing empty entries, also remove duplicate entries
        """
        # Fill the EnvironmentModifications instance
        env = EnvironmentModifications()
        # New variables
        new_variables = list(set(after) - set(before))
        # Variables that have been unset
        unset_variables = list(set(before) - set(after))
        # Variables that have been modified
        common_variables = set(before).intersection(set(after))
        modified_variables = [x for x in common_variables if before[x] != after[x]]
        # Consistent output order - looks nicer, easier comparison...
        new_variables.sort()
        unset_variables.sort()
        modified_variables.sort()

        def return_separator_if_any(*args):
            separators = ":", ";"
            for separator in separators:
                for arg in args:
                    if separator in arg:
                        return separator
            return None

        # Add variables to env.
        # Assume that variables with 'PATH' in the name or that contain
        # separators like ':' or ';' are more likely to be paths
        for variable_name in new_variables:
            sep = return_separator_if_any(after[variable_name])
            if sep:
                env.prepend_path(variable_name, after[variable_name], separator=sep)
            elif "PATH" in variable_name:
                env.prepend_path(variable_name, after[variable_name])
            else:
                # We just need to set the variable to the new value
                env.set(variable_name, after[variable_name])

        for variable_name in unset_variables:
            env.unset(variable_name)

        for variable_name in modified_variables:
            value_before = before[variable_name]
            value_after = after[variable_name]
            sep = return_separator_if_any(value_before, value_after)
            if sep:
                before_list = value_before.split(sep)
                after_list = value_after.split(sep)

                # Filter out empty strings
                before_list = list(filter(None, before_list))
                after_list = list(filter(None, after_list))

                # Remove duplicate entries (worse matching, bloats env)
                if clean:
                    before_list = list(dedupe(before_list))
                    after_list = list(dedupe(after_list))
                    # The reassembled cleaned entries
                    value_before = sep.join(before_list)
                    value_after = sep.join(after_list)

                # Paths that have been removed
                remove_list = [ii for ii in before_list if ii not in after_list]
                # Check that nothing has been added in the middle of
                # before_list
                remaining_list = [ii for ii in before_list if ii in after_list]
                try:
                    start = after_list.index(remaining_list[0])
                    end = after_list.index(remaining_list[-1])
                    search = sep.join(after_list[start : end + 1])
                except IndexError:
                    env.prepend_path(variable_name, value_after)
                    continue

                if search not in value_before:
                    # We just need to set the variable to the new value
                    env.prepend_path(variable_name, value_after)
                else:
                    try:
                        prepend_list = after_list[:start]
                        prepend_list.reverse()  # Preserve order after prepend
                    except KeyError:
                        prepend_list = []
                    try:
                        append_list = after_list[end + 1 :]
                    except KeyError:
                        append_list = []

                    for item in remove_list:
                        env.remove_path(variable_name, item)
                    for item in append_list:
                        env.append_path(variable_name, item)
                    for item in prepend_list:
                        env.prepend_path(variable_name, item)
            else:
                # We just need to set the variable to the new value
                env.set(variable_name, value_after)

        return env


def _set_or_unset_not_first(
    variable: str, changes: ModificationList, errstream: Callable[[str], None]
):
    """Check if we are going to set or unset something after other
    modifications have already been requested.
    """
    indexes = [
        ii
        for ii, item in enumerate(changes)
        if ii != 0 and isinstance(item, (SetEnv, UnsetEnv)) and not getattr(item, "force", False)
    ]
    if indexes:
        good = "\t    \t{}"
        nogood = "\t--->\t{}"
        errstream(f"Different requests to set/unset '{variable}' have been found")
        for idx, item in enumerate(changes):
            print_format = nogood if idx in indexes else good
            errstream(print_format.format(item.trace))


def validate(env: EnvironmentModifications, errstream: Callable[[str], None]):
    """Validates the environment modifications to check for the presence of
    suspicious patterns. Prompts a warning for everything that was found.

    Current checks:
    - set or unset variables after other changes on the same variable

    Args:
        env: list of environment modifications
        errstream: callable to log error messages
    """
    if not env.traced:
        return
    modifications = env.group_by_name()
    for variable, list_of_changes in sorted(modifications.items()):
        _set_or_unset_not_first(variable, list_of_changes, errstream)


def inspect_path(
    root: Path,
    inspections: MutableMapping[str, List[str]],
    exclude: Optional[Callable[[Path], bool]] = None,
) -> EnvironmentModifications:
    """Inspects ``root`` to search for the subdirectories in ``inspections``.
    Adds every path found to a list of prepend-path commands and returns it.

    Args:
        root: absolute path where to search for subdirectories
        inspections: maps relative paths to a list of environment
            variables that will be modified if the path exists. The
            modifications are not performed immediately, but stored in a
            command object that is returned to client
        exclude: optional callable. If present it must accept an
            absolute path and return True if it should be excluded from the
            inspection

    Examples:

    The following lines execute an inspection in ``/usr`` to search for
    ``/usr/include`` and ``/usr/lib64``. If found we want to prepend
    ``/usr/include`` to ``CPATH`` and ``/usr/lib64`` to ``MY_LIB64_PATH``.

        .. code-block:: python

            # Set up the dictionary containing the inspection
            inspections = {
                'include': ['CPATH'],
                'lib64': ['MY_LIB64_PATH']
            }

            # Get back the list of command needed to modify the environment
            env = inspect_path('/usr', inspections)

            # Eventually execute the commands
            env.apply_modifications()
    """
    if exclude is None:
        exclude = lambda x: False

    env = EnvironmentModifications()
    # Inspect the prefix to check for the existence of common directories
    for relative_path, variables in inspections.items():
        expected = os.path.join(root, os.path.normpath(relative_path))

        if os.path.isdir(expected) and not exclude(expected):
            for variable in variables:
                env.prepend_path(variable, expected)

    return env


@contextlib.contextmanager
def preserve_environment(*variables: str):
    """Ensures that the value of the environment variables passed as
    arguments is the same before entering to the context manager and after
    exiting it.

    Variables that are unset before entering the context manager will be
    explicitly unset on exit.

    Args:
        variables: list of environment variables to be preserved
    """
    cache = {}
    for var in variables:
        # The environment variable to be preserved might not be there.
        # In that case store None as a placeholder.
        cache[var] = os.environ.get(var, None)

    yield

    for var in variables:
        value = cache[var]
        msg = "[PRESERVE_ENVIRONMENT]"
        if value is not None:
            # Print a debug statement if the value changed
            if var not in os.environ:
                msg += ' {0} was unset, will be reset to "{1}"'
                tty.debug(msg.format(var, value))
            elif os.environ[var] != value:
                msg += ' {0} was set to "{1}", will be reset to "{2}"'
                tty.debug(msg.format(var, os.environ[var], value))
            os.environ[var] = value
        elif var in os.environ:
            msg += ' {0} was set to "{1}", will be unset'
            tty.debug(msg.format(var, os.environ[var]))
            del os.environ[var]


def environment_after_sourcing_files(
    *files: Union[Path, Tuple[str, ...]], **kwargs
) -> Dict[str, str]:
    """Returns a dictionary with the environment that one would have
    after sourcing the files passed as argument.

    Args:
        *files: each item can either be a string containing the path
            of the file to be sourced or a sequence, where the first element
            is the file to be sourced and the remaining are arguments to be
            passed to the command line

    Keyword Args:
        env (dict): the initial environment (default: current environment)
        shell (str): the shell to use (default: ``/bin/bash`` or ``cmd.exe`` (Windows))
        shell_options (str): options passed to the shell (default: ``-c`` or ``/C`` (Windows))
        source_command (str): the command to run (default: ``source``)
        suppress_output (str): redirect used to suppress output of command
            (default: ``&> /dev/null``)
        concatenate_on_success (str): operator used to execute a command
            only when the previous command succeeds (default: ``&&``)
    """
    # Set the shell executable that will be used to source files
    if sys.platform == "win32":
        shell_cmd = kwargs.get("shell", "cmd.exe")
        shell_options = kwargs.get("shell_options", "/C")
        suppress_output = kwargs.get("suppress_output", "")
        source_command = kwargs.get("source_command", "")
    else:
        shell_cmd = kwargs.get("shell", "/bin/bash")
        shell_options = kwargs.get("shell_options", "-c")
        suppress_output = kwargs.get("suppress_output", "&> /dev/null")
        source_command = kwargs.get("source_command", "source")
    concatenate_on_success = kwargs.get("concatenate_on_success", "&&")

    def _source_single_file(file_and_args, environment):
        shell_options_list = shell_options.split()

        source_file = [source_command]
        source_file.extend(x for x in file_and_args)
        source_file = " ".join(source_file)

        dump_cmd = "import os, json; print(json.dumps(dict(os.environ)))"
        dump_environment_cmd = sys.executable + f' -E -c "{dump_cmd}"'

        # Try to source the file
        source_file_arguments = " ".join(
            [source_file, suppress_output, concatenate_on_success, dump_environment_cmd]
        )

        with subprocess.Popen(
            [shell_cmd, *shell_options_list, source_file_arguments],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as shell:
            output, _ = shell.communicate()

        return json.loads(output)

    current_environment = kwargs.get("env", dict(os.environ))
    for file in files:
        # Normalize the input to the helper function
        if isinstance(file, str):
            file = (file,)

        current_environment = _source_single_file(file, environment=current_environment)

    return current_environment


def sanitize(
    environment: MutableMapping[str, str], exclude: List[str], include: List[str]
) -> Dict[str, str]:
    """Returns a copy of the input dictionary where all the keys that
    match an excluded pattern and don't match an included pattern are
    removed.

    Args:
        environment (dict): input dictionary
        exclude (list): literals or regex patterns to be excluded
        include (list): literals or regex patterns to be included
    """

    def set_intersection(fullset, *args):
        # A set intersection using string literals and regexs
        meta = "[" + re.escape("[$()*?[]^{|}") + "]"
        subset = fullset & set(args)  # As literal
        for name in args:
            if re.search(meta, name):
                pattern = re.compile(name)
                for k in fullset:
                    if re.match(pattern, k):
                        subset.add(k)
        return subset

    # Don't modify input, make a copy instead
    environment = dict(environment)

    # include supersedes any excluded items
    prune = set_intersection(set(environment), *exclude)
    prune -= set_intersection(prune, *include)
    for k in prune:
        environment.pop(k, None)

    return environment
