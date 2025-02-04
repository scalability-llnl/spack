# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from typing import Dict, List, Optional, Set, Tuple

import llnl.path
import llnl.util.lang
from llnl.util import tty
from llnl.util.filesystem import path_contains_subdirectory, paths_containing_libs

import spack.caches
import spack.schema.environment
import spack.spec
import spack.util.executable
import spack.util.libc
import spack.util.module_cmd
from spack.util.environment import filter_system_paths
from spack.util.file_cache import FileCache

#: regex for parsing linker lines
_LINKER_LINE = re.compile(r"^( *|.*[/\\])" r"(link|ld|([^/\\]+-)?ld|collect2)" r"[^/\\]*( |$)")

#: components of linker lines to ignore
_LINKER_LINE_IGNORE = re.compile(r"(collect2 version|^[A-Za-z0-9_]+=|/ldfe )")

#: regex to match linker search paths
_LINK_DIR_ARG = re.compile(r"^-L(.:)?(?P<dir>[/\\].*)")

#: regex to match linker library path arguments
_LIBPATH_ARG = re.compile(r"^[-/](LIBPATH|libpath):(?P<dir>.*)")


@llnl.path.system_path_filter
def parse_non_system_link_dirs(compiler_debug_output: str) -> List[str]:
    """Parses link paths out of compiler debug output.

    Args:
        compiler_debug_output: compiler debug output as a string

    Returns:
        Implicit link paths parsed from the compiler output
    """
    link_dirs = _parse_link_paths(compiler_debug_output)

    # Remove directories that do not exist. Some versions of the Cray compiler
    # report nonexistent directories
    link_dirs = filter_non_existing_dirs(link_dirs)

    # Return set of directories containing needed compiler libs, minus
    # system paths. Note that 'filter_system_paths' only checks for an
    # exact match, while 'in_system_subdirectory' checks if a path contains
    # a system directory as a subdirectory
    link_dirs = filter_system_paths(link_dirs)
    return list(p for p in link_dirs if not in_system_subdirectory(p))


def filter_non_existing_dirs(dirs):
    return [d for d in dirs if os.path.isdir(d)]


def in_system_subdirectory(path):
    system_dirs = [
        "/lib/",
        "/lib64/",
        "/usr/lib/",
        "/usr/lib64/",
        "/usr/local/lib/",
        "/usr/local/lib64/",
    ]
    return any(path_contains_subdirectory(path, x) for x in system_dirs)


def _parse_link_paths(string):
    """Parse implicit link paths from compiler debug output.

    This gives the compiler runtime library paths that we need to add to
    the RPATH of generated binaries and libraries.  It allows us to
    ensure, e.g., that codes load the right libstdc++ for their compiler.
    """
    lib_search_paths = False
    raw_link_dirs = []
    for line in string.splitlines():
        if lib_search_paths:
            if line.startswith("\t"):
                raw_link_dirs.append(line[1:])
                continue
            else:
                lib_search_paths = False
        elif line.startswith("Library search paths:"):
            lib_search_paths = True

        if not _LINKER_LINE.match(line):
            continue
        if _LINKER_LINE_IGNORE.match(line):
            continue
        tty.debug(f"implicit link dirs: link line: {line}")

        next_arg = False
        for arg in line.split():
            if arg in ("-L", "-Y"):
                next_arg = True
                continue

            if next_arg:
                raw_link_dirs.append(arg)
                next_arg = False
                continue

            link_dir_arg = _LINK_DIR_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group("dir")
                raw_link_dirs.append(link_dir)

            link_dir_arg = _LIBPATH_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group("dir")
                raw_link_dirs.append(link_dir)

    implicit_link_dirs = list()
    visited = set()
    for link_dir in raw_link_dirs:
        normalized_path = os.path.abspath(link_dir)
        if normalized_path not in visited:
            implicit_link_dirs.append(normalized_path)
            visited.add(normalized_path)

    tty.debug(f"implicit link dirs: result: {', '.join(implicit_link_dirs)}")
    return implicit_link_dirs


class CompilerPropertyDetector:

    def __init__(self, compiler_spec: spack.spec.Spec):
        assert compiler_spec.concrete, "only concrete compiler specs are allowed"
        self.spec = compiler_spec
        self.cache = COMPILER_CACHE

    @contextlib.contextmanager
    def compiler_environment(self):
        """Sets the environment to run this compiler"""

        # No modifications for Spack managed compilers
        if not self.spec.external:
            yield
            return

        # Avoid modifying os.environ if possible.
        environment = self.spec.extra_attributes.get("environment", {})
        modules = self.spec.external_modules or []
        if not self.spec.external_modules and not environment:
            yield
            return

        # store environment to replace later
        backup_env = os.environ.copy()

        try:
            # load modules and set env variables
            for module in modules:
                spack.util.module_cmd.load_module(module)

            # apply other compiler environment changes
            spack.schema.environment.parse(environment).apply_modifications()

            yield
        finally:
            # Restore environment regardless of whether inner code succeeded
            os.environ.clear()
            os.environ.update(backup_env)

    def _compile_dummy_c_source(self) -> Optional[str]:
        compiler_pkg = self.spec.package
        if getattr(compiler_pkg, "cc"):
            cc = compiler_pkg.cc
            ext = "c"
        else:
            cc = compiler_pkg.cxx
            ext = "cc"

        if not cc or not self.spec.package.verbose_flags:
            return None

        try:
            tmpdir = tempfile.mkdtemp(prefix="spack-implicit-link-info")
            fout = os.path.join(tmpdir, "output")
            fin = os.path.join(tmpdir, f"main.{ext}")

            with open(fin, "w", encoding="utf-8") as csource:
                csource.write(
                    "int main(int argc, char* argv[]) { (void)argc; (void)argv; return 0; }\n"
                )
            cc_exe = spack.util.executable.Executable(cc)

            if self.spec.external:
                compiler_flags = self.spec.extra_attributes.get("flags", {})
                for flag_type in [
                    "cflags" if cc == compiler_pkg.cc else "cxxflags",
                    "cppflags",
                    "ldflags",
                ]:
                    current_flags = compiler_flags.get(flag_type, "").strip()
                    if current_flags:
                        cc_exe.add_default_arg(*current_flags.split(" "))

            with self.compiler_environment():
                return cc_exe("-v", fin, "-o", fout, output=str, error=str)
        except spack.util.executable.ProcessError as pe:
            tty.debug(f"ProcessError: Command exited with non-zero status: {pe.long_message}")
            return None
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def compiler_verbose_output(self) -> Optional[str]:
        return self.cache.get(self.spec).c_compiler_output

    def default_dynamic_linker(self) -> Optional[str]:
        output = self.compiler_verbose_output()

        if not output:
            return None

        return spack.util.libc.parse_dynamic_linker(output)

    def default_libc(self) -> Optional[spack.spec.Spec]:
        """Determine libc targeted by the compiler from link line"""
        # technically this should be testing the target platform of the compiler, but we don't have
        # that, so stick to host platform for now.
        if sys.platform in ("darwin", "win32"):
            return None

        dynamic_linker = self.default_dynamic_linker()

        if dynamic_linker is None:
            return None

        return spack.util.libc.libc_from_dynamic_linker(dynamic_linker)

    def implicit_rpaths(self) -> List[str]:
        output = self.compiler_verbose_output()
        if output is None:
            return []

        link_dirs = parse_non_system_link_dirs(output)
        all_required_libs = list(self.spec.package.required_libs) + ["libc", "libc++", "libstdc++"]
        dynamic_linker = self.default_dynamic_linker()
        result = DefaultDynamicLinkerFilter(dynamic_linker)(
            paths_containing_libs(link_dirs, all_required_libs)
        )
        return list(result)


class DefaultDynamicLinkerFilter:
    """Remove rpaths to directories that are default search paths of the dynamic linker."""

    _CACHE: Dict[Optional[str], Set[Tuple[int, int]]] = {}

    def __init__(self, dynamic_linker: Optional[str]) -> None:
        if dynamic_linker not in DefaultDynamicLinkerFilter._CACHE:
            # Identify directories by (inode, device) tuple, which handles symlinks too.
            default_path_identifiers: Set[Tuple[int, int]] = set()
            if not dynamic_linker:
                self.default_path_identifiers = None
                return
            for path in spack.util.libc.default_search_paths_from_dynamic_linker(dynamic_linker):
                try:
                    s = os.stat(path)
                    if stat.S_ISDIR(s.st_mode):
                        default_path_identifiers.add((s.st_ino, s.st_dev))
                except OSError:
                    continue

            DefaultDynamicLinkerFilter._CACHE[dynamic_linker] = default_path_identifiers

        self.default_path_identifiers = DefaultDynamicLinkerFilter._CACHE[dynamic_linker]

    def is_dynamic_loader_default_path(self, p: str) -> bool:
        if self.default_path_identifiers is None:
            return False
        try:
            s = os.stat(p)
            return (s.st_ino, s.st_dev) in self.default_path_identifiers
        except OSError:
            return False

    def __call__(self, dirs: List[str]) -> List[str]:
        if not self.default_path_identifiers:
            return dirs
        return [p for p in dirs if not self.is_dynamic_loader_default_path(p)]


def dynamic_linker_filter_for(node: spack.spec.Spec) -> Optional[DefaultDynamicLinkerFilter]:
    compiler = compiler_spec(node)
    if compiler is None:
        return None
    detector = CompilerPropertyDetector(compiler)
    dynamic_linker = detector.default_dynamic_linker()
    if dynamic_linker is None:
        return None
    return DefaultDynamicLinkerFilter(dynamic_linker)


def compiler_spec(node: spack.spec.Spec) -> Optional[spack.spec.Spec]:
    """Returns the compiler spec associated with the node passed as argument.

    The function looks for a "c", "cxx", and "fortran" compiler in that order,
    and returns the first found. If none is found, returns None.
    """
    for language in ("c", "cxx", "fortran"):
        candidates = node.dependencies(virtuals=[language])
        if candidates:
            break
    else:
        return None

    return candidates[0]


class CompilerCacheEntry:
    """Deserialized cache entry for a compiler"""

    __slots__ = ("c_compiler_output",)

    def __init__(self, c_compiler_output: Optional[str]):
        self.c_compiler_output = c_compiler_output

    @property
    def empty(self) -> bool:
        """Sometimes the compiler is temporarily broken, preventing us from getting output. The
        call site determines if that is a problem."""
        return self.c_compiler_output is None

    @classmethod
    def from_dict(cls, data: Dict[str, Optional[str]]):
        if not isinstance(data, dict):
            raise ValueError(f"Invalid {cls.__name__} data")
        c_compiler_output = data.get("c_compiler_output")
        if not isinstance(c_compiler_output, (str, type(None))):
            raise ValueError(f"Invalid {cls.__name__} data")
        return cls(c_compiler_output)


class CompilerCache:
    """Base class for compiler output cache. Default implementation does not cache anything."""

    def value(self, compiler: spack.spec.Spec) -> Dict[str, Optional[str]]:
        return {"c_compiler_output": CompilerPropertyDetector(compiler)._compile_dummy_c_source()}

    def get(self, compiler: spack.spec.Spec) -> CompilerCacheEntry:
        return CompilerCacheEntry.from_dict(self.value(compiler))


class FileCompilerCache(CompilerCache):
    """Cache for compiler output, which is used to determine implicit link paths, the default libc
    version, and the compiler version."""

    name = os.path.join("compilers", "compilers.json")

    def __init__(self, cache: "FileCache") -> None:
        self.cache = cache
        self.cache.init_entry(self.name)
        self._data: Dict[str, Dict[str, Optional[str]]] = {}

    def _get_entry(self, key: str, *, allow_empty: bool) -> Optional[CompilerCacheEntry]:
        try:
            entry = CompilerCacheEntry.from_dict(self._data[key])
            return entry if allow_empty or not entry.empty else None
        except ValueError:
            del self._data[key]
        except KeyError:
            pass
        return None

    def get(self, compiler: spack.spec.Spec) -> CompilerCacheEntry:
        # Cache hit
        try:
            with self.cache.read_transaction(self.name) as f:
                assert f is not None
                self._data = json.loads(f.read())
                assert isinstance(self._data, dict)
        except (json.JSONDecodeError, AssertionError):
            self._data = {}

        key = self._key(compiler)
        value = self._get_entry(key, allow_empty=False)
        if value is not None:
            return value

        # Cache miss
        with self.cache.write_transaction(self.name) as (old, new):
            try:
                assert old is not None
                self._data = json.loads(old.read())
                assert isinstance(self._data, dict)
            except (json.JSONDecodeError, AssertionError):
                self._data = {}

            # Use cache entry that may have been created by another process in the meantime.
            entry = self._get_entry(key, allow_empty=True)

            # Finally compute the cache entry
            if entry is None:
                self._data[key] = self.value(compiler)
                entry = CompilerCacheEntry.from_dict(self._data[key])

            new.write(json.dumps(self._data, separators=(",", ":")))

            return entry

    def _key(self, compiler: spack.spec.Spec) -> str:
        as_bytes = json.dumps(compiler.to_dict(), separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(as_bytes).hexdigest()


def _make_compiler_cache():
    return FileCompilerCache(spack.caches.MISC_CACHE)


COMPILER_CACHE: CompilerCache = llnl.util.lang.Singleton(_make_compiler_cache)  # type: ignore
