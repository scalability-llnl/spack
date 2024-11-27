# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import BinaryIO, Optional, Tuple

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, visit_directory_tree

from spack.util.elf import ElfParsingError, parse_elf


def should_keep(path: bytes) -> bool:
    """Return True iff path starts with $ (typically for $ORIGIN/${ORIGIN}) or is
    absolute and exists."""
    return path.startswith(b"$") or (os.path.isabs(path) and os.path.lexists(path))


def _drop_redundant_rpaths(f: BinaryIO) -> Optional[Tuple[bytes, bytes]]:
    """Drop redundant entries from rpath.

    Args:
        f: File object to patch opened in r+b mode.

    Returns:
        A tuple of the old and new rpath if the rpath was patched, None otherwise.
    """
    try:
        elf = parse_elf(f, interpreter=False, dynamic_section=True)
    except ElfParsingError:
        return None

    # Nothing to do.
    if not elf.has_rpath:
        return None

    old_rpath_str = elf.dt_rpath_str
    new_rpath_str = b":".join(p for p in old_rpath_str.split(b":") if should_keep(p))

    # Nothing to write.
    if old_rpath_str == new_rpath_str:
        return None

    # Pad with 0 bytes.
    pad = len(old_rpath_str) - len(new_rpath_str)

    # This can never happen since we're filtering, but lets be defensive.
    if pad < 0:
        return None

    # The rpath is at a given offset in the string table used by the
    # dynamic section.
    rpath_offset = elf.pt_dynamic_strtab_offset + elf.rpath_strtab_offset

    f.seek(rpath_offset)
    f.write(new_rpath_str + b"\x00" * pad)
    return old_rpath_str, new_rpath_str


def drop_redundant_rpaths(path: str) -> Optional[Tuple[bytes, bytes]]:
    """Drop redundant entries from rpath.

    Args:
        path: Path to a potential ELF file to patch.

    Returns:
        A tuple of the old and new rpath if the rpath was patched, None otherwise.
    """
    try:
        with open(path, "r+b") as f:
            return _drop_redundant_rpaths(f)
    except OSError:
        return None


class ElfFilesWithRPathVisitor(BaseDirectoryVisitor):
    """Visitor that collects all elf files that have an rpath"""

    def __init__(self):
        # Keep track of what hardlinked files we've already visited.
        self.visited = set()

    def visit_file(self, root, rel_path, depth):
        filepath = os.path.join(root, rel_path)
        s = os.lstat(filepath)
        identifier = (s.st_ino, s.st_dev)

        # We're hitting a hardlink or symlink of an excluded lib, no need to parse.
        if s.st_nlink > 1:
            if identifier in self.visited:
                return
            self.visited.add(identifier)

        result = drop_redundant_rpaths(filepath)

        if result is not None:
            old, new = result
            tty.debug(f"Patched rpath in {rel_path} from {old!r} to {new!r}")

    def visit_symlinked_file(self, root, rel_path, depth):
        pass

    def before_visit_dir(self, root, rel_path, depth):
        # Always enter dirs
        return True

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        # Never enter symlinked dirs
        return False


def post_install(spec, explicit=None):
    # Skip externals
    if spec.external:
        return

    # Only enable on platforms using ELF.
    if not spec.satisfies("platform=linux"):
        return

    visit_directory_tree(spec.prefix, ElfFilesWithRPathVisitor())
