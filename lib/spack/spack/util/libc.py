# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import re
import shlex
import sys
from subprocess import PIPE, run
from typing import List, Optional

import spack.spec
import spack.util.elf


def _libc_from_ldd(ldd: str) -> Optional["spack.spec.Spec"]:
    try:
        result = run([ldd, "--version"], stdout=PIPE, stderr=PIPE, check=False)
        stdout = result.stdout.decode("utf-8")
    except Exception:
        return None

    if not re.search(r"\bFree Software Foundation\b", stdout):
        return None

    version_str = re.match(r".+\(.+\) (.+)", stdout)
    if not version_str:
        return None
    try:
        return spack.spec.Spec(f"glibc@={version_str.group(1)}")
    except Exception:
        return None


def default_search_paths_from_dynamic_linker(dynamic_linker: str) -> List[str]:
    """If the dynamic linker is glibc at a certain version, we can query the hard-coded library
    search paths"""
    try:
        result = run([dynamic_linker, "--help"], stdout=PIPE, stderr=PIPE, check=False)
        assert result.returncode == 0
        out = result.stdout.decode("utf-8")
    except Exception:
        return []

    return [
        match.group(1).strip()
        for match in re.finditer(r"^  (/.+) \(system search path\)$", out, re.MULTILINE)
    ]


def libc_from_dynamic_linker(dynamic_linker: str) -> Optional["spack.spec.Spec"]:
    if not os.path.exists(dynamic_linker):
        return None

    # The dynamic linker is usually installed in the same /lib(64)?/ld-*.so path across all
    # distros. The rest of libc is elsewhere, e.g. /usr. Typically the dynamic linker is then
    # a symlink into /usr/lib, which we use to for determining the actual install prefix of
    # libc.
    realpath = os.path.realpath(dynamic_linker)

    prefix = os.path.dirname(realpath)
    # Remove the multiarch suffix if it exists
    if os.path.basename(prefix) not in ("lib", "lib64"):
        prefix = os.path.dirname(prefix)

    # Non-standard install layout -- just bail.
    if os.path.basename(prefix) not in ("lib", "lib64"):
        return None

    prefix = os.path.dirname(prefix)

    # Now try to figure out if glibc or musl, which is the only ones we support.
    # In recent glibc we can simply execute the dynamic loader. In musl that's always the case.
    try:
        result = run([dynamic_linker, "--version"], stdout=PIPE, stderr=PIPE, check=False)
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
    except Exception:
        return None

    # musl prints to stderr
    if stderr.startswith("musl libc"):
        version_str = re.search(r"^Version (.+)$", stderr, re.MULTILINE)
        if not version_str:
            return None
        try:
            spec = spack.spec.Spec(f"musl@={version_str.group(1)}")
            spec.external_path = prefix
            return spec
        except Exception:
            return None
    elif re.search(r"\bFree Software Foundation\b", stdout):
        # output is like "ld.so (...) stable release version 2.33."
        match = re.search(r"version (\d+\.\d+(?:\.\d+)?)", stdout)
        if not match:
            return None
        try:
            version = match.group(1)
            spec = spack.spec.Spec(f"glibc@={version}")
            spec.external_path = prefix
            return spec
        except Exception:
            return None
    else:
        # Could not get the version by running the dynamic linker directly. Instead locate `ldd`
        # relative to the dynamic linker.
        ldd = os.path.join(prefix, "bin", "ldd")
        if not os.path.exists(ldd):
            # If `/lib64/ld.so` was not a symlink to `/usr/lib/ld.so` we can try to use /usr as
            # prefix. This is the case on ubuntu 18.04 where /lib != /usr/lib.
            if prefix != "/":
                return None
            prefix = "/usr"
            ldd = os.path.join(prefix, "bin", "ldd")
            if not os.path.exists(ldd):
                return None
        maybe_spec = _libc_from_ldd(ldd)
        if not maybe_spec:
            return None
        maybe_spec.external_path = prefix
        return maybe_spec


def libc_from_current_python_process() -> Optional["spack.spec.Spec"]:
    if not sys.executable:
        return None

    dynamic_linker = spack.util.elf.pt_interp(sys.executable)

    if not dynamic_linker:
        return None

    return libc_from_dynamic_linker(dynamic_linker)


def startfile_prefix(prefix: str, compatible_with: str = sys.executable) -> Optional[str]:
    # Search for crt1.o at max depth 2 compatible with the ELF file provided in compatible_with.
    # This is useful for finding external libc startfiles on a multiarch system.
    try:
        compat = spack.util.elf.get_elf_compat(compatible_with)
        accept = lambda path: spack.util.elf.get_elf_compat(path) == compat
    except Exception:
        accept = lambda path: True

    stack = [(0, prefix)]
    while stack:
        depth, path = stack.pop()
        try:
            iterator = os.scandir(path)
        except OSError:
            continue
        with iterator:
            for entry in iterator:
                try:
                    if entry.is_dir(follow_symlinks=True):
                        if depth < 2:
                            stack.append((depth + 1, entry.path))
                    elif entry.name == "crt1.o" and accept(entry.path):
                        return path
                except Exception:
                    continue
    return None


def parse_dynamic_linker(output: str):
    """Parse -dynamic-linker /path/to/ld.so from compiler output"""
    for line in reversed(output.splitlines()):
        if "-dynamic-linker" not in line:
            continue
        args = shlex.split(line)

        for idx in reversed(range(1, len(args))):
            arg = args[idx]
            if arg == "-dynamic-linker" or args == "--dynamic-linker":
                return args[idx + 1]
            elif arg.startswith("--dynamic-linker=") or arg.startswith("-dynamic-linker="):
                return arg.split("=", 1)[1]


def libc_include_dir_from_startfile_prefix(
    libc_prefix: str, startfile_prefix: str
) -> Optional[str]:
    """Heuristic to determine the glibc include directory from the startfile prefix. Replaces
    $libc_prefix/lib*/<multiarch> with $libc_prefix/include/<multiarch>. This function does not
    check if the include directory actually exists or is correct."""
    parts = os.path.relpath(startfile_prefix, libc_prefix).split(os.path.sep)
    if parts[0] not in ("lib", "lib64", "libx32", "lib32"):
        return None
    parts[0] = "include"
    return os.path.join(libc_prefix, *parts)
