# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import os

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, visit_directory_tree
from llnl.util.lang import stable_partition

import spack.config
import spack.error
import spack.util.elf as elf

skip_list = frozenset(
    [
        # kernel
        b"linux-vdso",
        # glibc
        b"ld-linux-x86-64",
        b"libc",
        b"libdl",
        b"libgcc_s",
        b"libm",
        b"libmemusage",
        b"libmvec",
        b"libnsl",
        b"libnss_compat",
        b"libnss_db",
        b"libnss_dns",
        b"libnss_files",
        b"libnss_hesiod",
        b"libpcprofile",
        b"libpthread",
        b"libresolv",
        b"librt",
        b"libSegFault",
        b"libthread_db",
        b"libutil",
        # gcc
        b"libasan",
        b"libatomic",
        b"libcc1",
        b"libgcc_s",
        b"libgfortran",
        b"libgomp",
        b"libitm",
        b"liblsan",
        b"libquadmath",
        b"libssp",
        b"libstdc++",
        b"libtsan",
        b"libubsan",
    ]
)


def is_compatible(parent, child):
    return (
        child.elf_hdr.e_type == elf.ELF_CONSTANTS.ET_DYN
        and parent.is_little_endian == child.is_little_endian
        and parent.is_64_bit == child.is_64_bit
        and parent.elf_hdr.e_machine == child.elf_hdr.e_machine
    )


def candidate_matches(current_elf, candidate_path):
    try:
        with open(candidate_path, "rb") as g:
            return is_compatible(current_elf, elf.parse_elf(g))
    except (IOError, elf.ElfParsingError):
        return False


def should_be_searched(needed_lib):
    offset = needed_lib.find(b".so")
    return offset == -1 or needed_lib[:offset] not in skip_list


class Problem:
    def __init__(self, resolved, unresolved):
        self.resolved = resolved
        self.unresolved = unresolved


class ResolveSharedElfLibDepsVisitor(BaseDirectoryVisitor):
    def __init__(self):
        self.problems = {}

    def visit_file(self, root, rel_path, depth):
        # We work with byte strings for paths.
        path = os.path.join(root, rel_path).encode("utf-8")

        # For $ORIGIN interpolation: should not have trailing dir seperator.
        origin = os.path.dirname(path)

        # Retrieve the needed libs + rpaths.
        try:
            with open(path, "rb") as f:
                parsed_elf = elf.parse_elf(f, interpreter=False, dynamic_section=True)
        except (IOError, elf.ElfParsingError):
            # Not dealing with a valid ELF file.
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

        # Relative rpaths exist (they're relative to current working dir, really bad).
        rpaths, rpaths_rel = stable_partition(rpaths, os.path.isabs)
        if rpaths_rel:
            raise Exception("Relative rpaths in {!r} detected {!r}".format(path, rpaths_rel))

        # If there's a / in the needed lib, it's opened directly, otherwise it needs
        # a search.
        direct_libs, search_libs = stable_partition(needed_libs, lambda x: b"/" in x)

        # Also direct libs can come in relative and absolute path flavor, we don't like
        # finding libraries relative to the current working directory, so error when
        # those are found.
        direct_libs, direct_libs_rel = stable_partition(direct_libs, os.path.isabs)

        if direct_libs_rel:
            raise Exception("Needed libraries by relative path {!r}".format(direct_libs_rel))

        # Now we remove the libraries that we consider system libraries.
        search_libs = list(filter(should_be_searched, search_libs))

        # Look for issues.
        resolved = {}
        unresolved = []

        for lib in search_libs:
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

        # A problem :(
        if unresolved:
            self.problems[rel_path] = Problem(resolved, unresolved)

    def visit_symlinked_file(self, root, rel_path, depth):
        pass

    def before_visit_dir(self, root, rel_path, depth):
        return True

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        return False


class CannotLocateSharedLibraries(Exception):
    pass


def maybe_decode(byte_str):
    try:
        return byte_str.decode("utf-8")
    except UnicodeDecodeError:
        return byte_str


def post_install(spec):
    """
    Check whether all ELF files participating in dynamic linking can locate libraries
    in dt_needed referred to by name (not by path).
    """
    if spec.external or spec.platform not in ("linux", "freebsd", "netbsd", "openbsd", "solaris"):
        return

    visitor = ResolveSharedElfLibDepsVisitor()
    visit_directory_tree(spec.prefix, visitor)

    # All good?
    if not visitor.problems:
        return

    # For now just list the issues (print it in ldd style, except we don't recurse)
    output = io.StringIO()
    output.write("Not all executables/libraries can resolve their dependencies:\n")
    for path, problem in visitor.problems.items():
        output.write(path)
        output.write("\n")
        for needed, full_path in problem.resolved.items():
            output.write("        ")
            if needed == full_path:
                output.write(maybe_decode(needed))
            else:
                output.write("{} => {}".format(maybe_decode(needed), maybe_decode(full_path)))
            output.write("\n")
        for not_found in problem.unresolved:
            output.write("        {} => not found\n".format(maybe_decode(not_found)))
        output.write("\n")

    # Strict mode = install failure
    if spack.config.get("config:shared_linking:strict"):
        raise CannotLocateSharedLibraries(output.getvalue())

    tty.error(output.getvalue())
