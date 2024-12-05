# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, visit_directory_tree
from llnl.util.lang import elide_list

import spack.bootstrap
import spack.config
import spack.relocate
from spack.util.elf import ElfParsingError, parse_elf


def is_shared_library_elf(filepath):
    """Return true if filepath is most a shared library.
    Our definition of a shared library for ELF requires:
    1. a dynamic section,
    2. a soname OR lack of interpreter.
    The problem is that PIE objects (default on Ubuntu) are
    ET_DYN too, and not all shared libraries have a soname...
    no interpreter is typically the best indicator then."""
    try:
        with open(filepath, "rb") as f:
            elf = parse_elf(f, interpreter=True, dynamic_section=True)
            return elf.has_pt_dynamic and (elf.has_soname or not elf.has_pt_interp)
    except (IOError, OSError, ElfParsingError):
        return False


class SharedLibrariesVisitor(BaseDirectoryVisitor):
    """Visitor that collects all shared libraries in a prefix, with the
    exception of an exclude list."""

    def __init__(self, exclude_list):
        # List of file and directory names to be excluded
        self.exclude_list = frozenset(exclude_list)

        # Map from (ino, dev) -> path. We need 1 path per file, if there are hardlinks,
        # we don't need to store the path multiple times.
        self.libraries = dict()

        # Set of (ino, dev) pairs (excluded by symlinks).
        self.excluded_through_symlink = set()

    def visit_file(self, root, rel_path, depth):
        # Check if excluded
        basename = os.path.basename(rel_path)
        if basename in self.exclude_list:
            return

        filepath = os.path.join(root, rel_path)
        s = os.lstat(filepath)
        identifier = (s.st_ino, s.st_dev)

        # We're hitting a hardlink or symlink of an excluded lib, no need to parse.
        if identifier in self.libraries or identifier in self.excluded_through_symlink:
            return

        # Register the file if it's a shared lib that needs to be patched.
        if is_shared_library_elf(filepath):
            self.libraries[identifier] = rel_path

    def visit_symlinked_file(self, root, rel_path, depth):
        # We don't need to follow the symlink and parse the file, since we will hit
        # it by recursing the prefix anyways. We only need to check if the target
        # should be excluded based on the filename of the symlink. E.g. when excluding
        # libf.so, which is a symlink to libf.so.1.2.3, we keep track of the stat data
        # of the latter.
        basename = os.path.basename(rel_path)
        if basename not in self.exclude_list:
            return

        # Register the (ino, dev) pair as ignored (if the symlink is not dangling)
        filepath = os.path.join(root, rel_path)
        try:
            s = os.stat(filepath)
        except OSError:
            return
        self.excluded_through_symlink.add((s.st_ino, s.st_dev))

    def before_visit_dir(self, root, rel_path, depth):
        # Allow skipping over directories. E.g. `<prefix>/lib/stubs` can be skipped by
        # adding `"stubs"` to the exclude list.
        return os.path.basename(rel_path) not in self.exclude_list

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        # Never enter symlinked dirs, since we don't want to leave the prefix, and
        # we'll enter the target dir inside the prefix anyways since we're recursing
        # everywhere.
        return False

    def get_shared_libraries_relative_paths(self):
        """Get the libraries that should be patched, with the excluded libraries
        removed."""
        for identifier in self.excluded_through_symlink:
            self.libraries.pop(identifier, None)

        return [rel_path for rel_path in self.libraries.values()]


def patch_sonames(patchelf, root, rel_paths):
    """Set the soname to the file's own path for a list of
    given shared libraries."""
    fixed = []
    for rel_path in rel_paths:
        filepath = os.path.join(root, rel_path)
        normalized = os.path.normpath(filepath)
        args = ["--set-soname", normalized, normalized]
        output = patchelf(*args, output=str, error=str, fail_on_error=False)
        if patchelf.returncode == 0:
            fixed.append(rel_path)
        else:
            # Note: treat as warning to avoid (long) builds to fail post-install.
            tty.warn("patchelf: failed to set soname of {}: {}".format(normalized, output.strip()))
    return fixed


def find_and_patch_sonames(prefix, exclude_list, patchelf):
    # Locate all shared libraries in the prefix dir of the spec, excluding
    # the ones set in the non_bindable_shared_objects property.
    visitor = SharedLibrariesVisitor(exclude_list)
    visit_directory_tree(prefix, visitor)

    # Patch all sonames.
    relative_paths = visitor.get_shared_libraries_relative_paths()
    return patch_sonames(patchelf, prefix, relative_paths)


def post_install(spec, explicit=None):
    # Skip if disabled
    if not spack.config.get("config:shared_linking:bind", False):
        return

    # Skip externals
    if spec.external:
        return

    # Only enable on platforms using ELF.
    if not spec.satisfies("platform=linux"):
        return

    # Disable this hook when bootstrapping, to avoid recursion.
    if spack.bootstrap.is_bootstrapping():
        return

    # Should failing to locate patchelf be a hard error?
    patchelf = spack.relocate._patchelf()
    if not patchelf:
        return

    fixes = find_and_patch_sonames(spec.prefix, spec.package.non_bindable_shared_objects, patchelf)

    if not fixes:
        return

    # Unfortunately this does not end up in the build logs.
    tty.info(
        "{}: Patched {} {}: {}".format(
            spec.name,
            len(fixes),
            "soname" if len(fixes) == 1 else "sonames",
            ", ".join(elide_list(fixes, max_num=5)),
        )
    )
