# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import fnmatch
import os
import re
from typing import IO, Dict, List

from llnl.util.filesystem import BaseDirectoryVisitor
from llnl.util.lang import stable_partition

import spack.util.elf as elf

#: Patterns for names of libraries that are allowed to be unresolved when *just* looking at RPATHs
#: added by Spack. These are libraries outside of Spack's control, and assumed to be located in
#: default search paths of the dynamic linker.
ALLOW_UNRESOLVED = [
    # kernel
    "linux-vdso.so.*",
    "libselinux.so.*",
    # musl libc
    "ld-musl-*.so.*",
    # glibc
    "ld-linux*.so.*",
    "ld64.so.*",
    "libanl.so.*",
    "libc.so.*",
    "libdl.so.*",
    "libm.so.*",
    "libmemusage.so.*",
    "libmvec.so.*",
    "libnsl.so.*",
    "libnss_compat.so.*",
    "libnss_db.so.*",
    "libnss_dns.so.*",
    "libnss_files.so.*",
    "libnss_hesiod.so.*",
    "libpcprofile.so.*",
    "libpthread.so.*",
    "libresolv.so.*",
    "librt.so.*",
    "libSegFault.so.*",
    "libthread_db.so.*",
    "libutil.so.*",
    # gcc -- this is required even with gcc-runtime, because e.g. libstdc++ depends on libgcc_s,
    # but the binaries we copy from the compiler don't have an $ORIGIN rpath.
    "libasan.so.*",
    "libatomic.so.*",
    "libcc1.so.*",
    "libgcc_s.so.*",
    "libgfortran.so.*",
    "libgomp.so.*",
    "libitm.so.*",
    "liblsan.so.*",
    "libquadmath.so.*",
    "libssp.so.*",
    "libstdc++.so.*",
    "libtsan.so.*",
    "libubsan.so.*",
    # systemd
    "libudev.so.*",
    # cuda driver
    "libcuda.so.*",
    # intel-oneapi-runtime
    "libur_loader.so.*",
]


def is_compatible(parent: elf.ElfFile, child: elf.ElfFile) -> bool:
    return (
        child.elf_hdr.e_type == elf.ELF_CONSTANTS.ET_DYN
        and parent.is_little_endian == child.is_little_endian
        and parent.is_64_bit == child.is_64_bit
        and parent.elf_hdr.e_machine == child.elf_hdr.e_machine
    )


def candidate_matches(current_elf: elf.ElfFile, candidate_path: bytes) -> bool:
    try:
        with open(candidate_path, "rb") as g:
            return is_compatible(current_elf, elf.parse_elf(g))
    except (OSError, elf.ElfParsingError):
        return False


class Problem:
    def __init__(
        self, resolved: Dict[bytes, bytes], unresolved: List[bytes], relative_rpaths: List[bytes]
    ) -> None:
        self.resolved = resolved
        self.unresolved = unresolved
        self.relative_rpaths = relative_rpaths


class ResolveSharedElfLibDepsVisitor(BaseDirectoryVisitor):
    def __init__(self, allow_unresolved_patterns: List[str]) -> None:
        self.problems: Dict[str, Problem] = {}
        self._allow_unresolved_regex = re.compile(
            "|".join(fnmatch.translate(x) for x in allow_unresolved_patterns)
        )

    def allow_unresolved(self, needed: bytes) -> bool:
        try:
            name = needed.decode("utf-8")
        except UnicodeDecodeError:
            return False
        return bool(self._allow_unresolved_regex.match(name))

    def visit_file(self, root: str, rel_path: str, depth: int) -> None:
        # We work with byte strings for paths.
        path = os.path.join(root, rel_path).encode("utf-8")

        # For $ORIGIN interpolation: should not have trailing dir seperator.
        origin = os.path.dirname(path)

        # Retrieve the needed libs + rpaths.
        try:
            with open(path, "rb") as f:
                parsed_elf = elf.parse_elf(f, interpreter=False, dynamic_section=True)
        except (OSError, elf.ElfParsingError):
            # Not dealing with an invalid ELF file.
            return

        # If there's no needed libs all is good
        if not parsed_elf.has_needed:
            return

        # Get the needed libs and rpaths (notice: byte strings)
        # Don't force an encoding cause paths are just a bag of bytes.
        needed_libs = parsed_elf.dt_needed_strs

        rpaths = parsed_elf.dt_rpath_str.split(b":") if parsed_elf.has_rpath else []

        # We only interpolate $ORIGIN, not $LIB and $PLATFORM, they're not really
        # supported in general. Also remove empty paths.
        rpaths = [x.replace(b"$ORIGIN", origin) for x in rpaths if x]

        # Do not allow relative rpaths (they are relative to the current working directory)
        rpaths, relative_rpaths = stable_partition(rpaths, os.path.isabs)

        # If there's a / in the needed lib, it's opened directly, otherwise it needs
        # a search.
        direct_libs, search_libs = stable_partition(needed_libs, lambda x: b"/" in x)

        # Do not allow relative paths in direct libs (they are relative to the current working
        # directory)
        direct_libs, unresolved = stable_partition(direct_libs, os.path.isabs)

        resolved: Dict[bytes, bytes] = {}

        for lib in search_libs:
            if self.allow_unresolved(lib):
                continue
            for rpath in rpaths:
                candidate = os.path.join(rpath, lib)
                if candidate_matches(parsed_elf, candidate):
                    resolved[lib] = candidate
                    break
            else:
                unresolved.append(lib)

        # Check if directly opened libs are compatible
        for lib in direct_libs:
            if candidate_matches(parsed_elf, lib):
                resolved[lib] = lib
            else:
                unresolved.append(lib)

        if unresolved or relative_rpaths:
            self.problems[rel_path] = Problem(resolved, unresolved, relative_rpaths)

    def visit_symlinked_file(self, root: str, rel_path: str, depth: int) -> None:
        pass

    def before_visit_dir(self, root: str, rel_path: str, depth: int) -> bool:
        # There can be binaries in .spack/test which shouldn't be checked.
        if rel_path == ".spack":
            return False
        return True

    def before_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> bool:
        return False

    def write(self, output: IO[str], *, indent=0, brief: bool = False) -> None:
        indent_str = " " * indent
        for path, problem in self.problems.items():
            output.write(indent_str)
            output.write(path)
            output.write("\n")
            if not brief:
                for needed, full_path in problem.resolved.items():
                    output.write(indent_str)
                    output.write("        ")
                    if needed == full_path:
                        output.write(_decode_or_raw(needed))
                    else:
                        output.write(f"{_decode_or_raw(needed)} => {_decode_or_raw(full_path)}")
                    output.write("\n")
            for not_found in problem.unresolved:
                output.write(indent_str)
                output.write(f"        {_decode_or_raw(not_found)} => not found\n")
            for relative_rpath in problem.relative_rpaths:
                output.write(indent_str)
                output.write(f"        {_decode_or_raw(relative_rpath)} => relative rpath\n")


def _decode_or_raw(byte_str: bytes) -> str:
    try:
        return byte_str.decode("utf-8")
    except UnicodeDecodeError:
        return f"{byte_str!r}"
