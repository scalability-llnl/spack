# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LinkTree class for setting up trees of symbolic links."""

import filecmp
import os
import shutil
from typing import Callable, Dict, List, Optional, Tuple

import llnl.util.tty as tty
from llnl.util.filesystem import BaseDirectoryVisitor, mkdirp, touch, traverse_tree
from llnl.util.symlink import islink, symlink

__all__ = ["LinkTree"]

empty_file_name = ".spack-empty"


def remove_link(src, dest):
    if not islink(dest):
        raise ValueError("%s is not a link tree!" % dest)
    # remove if dest is a hardlink/symlink to src; this will only
    # be false if two packages are merged into a prefix and have a
    # conflicting file
    if filecmp.cmp(src, dest, shallow=True):
        os.remove(dest)


class MergeConflict:
    """
    The invariant here is that src_a and src_b are both mapped
    to dst:

        project(src_a) == project(src_b) == dst
    """

    def __init__(self, dst, src_a=None, src_b=None):
        self.dst = dst
        self.src_a = src_a
        self.src_b = src_b


class SourceMergeVisitor(BaseDirectoryVisitor):
    """
    Visitor that produces actions:
    - An ordered list of directories to create in dst
    - A list of files to link in dst
    - A list of merge conflicts in dst/
    """

    def __init__(self, ignore: Optional[Callable[[str], bool]] = None):
        self.ignore = ignore if ignore is not None else lambda f: False

        # When mapping <src root> to <dst root>/<projection>, we need to prepend the <projection>
        # bit to the relative path in the destination dir.
        self.projection: str = ""

        # Two files f and g conflict if they are not os.path.samefile(f, g) and they are both
        # projected to the same destination file. These conflicts are not necessarily fatal, and
        # can be resolved or ignored. For example <prefix>/LICENSE or
        # <site-packages>/<namespace>/__init__.py conflicts can be ignored).
        self.file_conflicts: List[MergeConflict] = []

        # When we have to create a dir where a file is, or a file where a dir is, we have fatal
        # errors, listed here.
        self.fatal_conflicts: List[MergeConflict] = []

        # What directories we have to make; this is an ordered dict, so that we have a fast lookup
        # and can run mkdir in order.
        self.directories: Dict[str, Tuple[str, str]] = {}

        # Files to link. Maps dst_rel to (src_root, src_rel). This is an ordered dict, where files
        # are guaranteed to be grouped by src_root in the order they were visited.
        self.files: Dict[str, Tuple[str, str]] = {}

    def before_visit_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """
        Register a directory if dst / rel_path is not blocked by a file or ignored.
        """
        proj_rel_path = os.path.join(self.projection, rel_path)

        if self.ignore(rel_path):
            # Don't recurse when dir is ignored.
            return False
        elif proj_rel_path in self.files:
            # Can't create a dir where a file is.
            src_a_root, src_a_relpath = self.files[proj_rel_path]
            self.fatal_conflicts.append(
                MergeConflict(
                    dst=proj_rel_path,
                    src_a=os.path.join(src_a_root, src_a_relpath),
                    src_b=os.path.join(root, rel_path),
                )
            )
            return False
        elif proj_rel_path in self.directories:
            # No new directory, carry on.
            return True
        else:
            # Register new directory.
            self.directories[proj_rel_path] = (root, rel_path)
            return True

    def before_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """
        Replace symlinked dirs with actual directories when possible in low depths,
        otherwise handle it as a file (i.e. we link to the symlink).

        Transforming symlinks into dirs makes it more likely we can merge directories,
        e.g. when <prefix>/lib -> <prefix>/subdir/lib.

        We only do this when the symlink is pointing into a subdirectory from the
        symlink's directory, to avoid potential infinite recursion; and only at a
        constant level of nesting, to avoid potential exponential blowups in file
        duplication.
        """
        if self.ignore(rel_path):
            return False

        # Only follow symlinked dirs in <prefix>/**/**/*
        if depth > 1:
            handle_as_dir = False
        else:
            # Only follow symlinked dirs when pointing deeper
            src = os.path.join(root, rel_path)
            real_parent = os.path.realpath(os.path.dirname(src))
            real_child = os.path.realpath(src)
            handle_as_dir = real_child.startswith(real_parent)

        if handle_as_dir:
            return self.before_visit_dir(root, rel_path, depth)

        self.visit_file(root, rel_path, depth)
        return False

    def visit_file(self, root: str, rel_path: str, depth: int, *, symlink: bool = False) -> None:
        proj_rel_path = os.path.join(self.projection, rel_path)

        if self.ignore(rel_path):
            pass
        elif proj_rel_path in self.directories:
            # Can't create a file where a dir is; fatal error
            self.fatal_conflicts.append(
                MergeConflict(
                    dst=proj_rel_path,
                    src_a=os.path.join(*self.directories[proj_rel_path]),
                    src_b=os.path.join(root, rel_path),
                )
            )
        elif proj_rel_path in self.files:
            # When two files project to the same path, they conflict iff they are distinct.
            # If they are the same (i.e. one links to the other), register regular files rather
            # than symlinks. The reason is that in copy-type views, we need a copy of the actual
            # file, not the symlink.

            src_a = os.path.join(*self.files[proj_rel_path])
            src_b = os.path.join(root, rel_path)

            try:
                samefile = os.path.samefile(src_a, src_b)
            except OSError:
                samefile = False

            if not samefile:
                # Distinct files produce a conflict.
                self.file_conflicts.append(
                    MergeConflict(dst=proj_rel_path, src_a=src_a, src_b=src_b)
                )
                return

            if not symlink:
                # Remove the link in favor of the actual file. The del is necessary to maintain the
                # order of the files dict, which is grouped by root.
                del self.files[proj_rel_path]
                self.files[proj_rel_path] = (root, rel_path)

        else:
            # Otherwise register this file to be linked.
            self.files[proj_rel_path] = (root, rel_path)

    def visit_symlinked_file(self, root: str, rel_path: str, depth: int) -> None:
        # Treat symlinked files as ordinary files (without "dereferencing")
        self.visit_file(root, rel_path, depth, symlink=True)

    def set_projection(self, projection: str) -> None:
        self.projection = os.path.normpath(projection)

        # Todo, is this how to check in general for empty projection?
        if self.projection == ".":
            self.projection = ""
            return

        # If there is a projection, we'll also create the directories
        # it consists of, and check whether that's causing conflicts.
        path = ""
        for part in self.projection.split(os.sep):
            path = os.path.join(path, part)
            if path not in self.files:
                self.directories[path] = ("<projection>", path)
            else:
                # Can't create a dir where a file is.
                src_a_root, src_a_relpath = self.files[path]
                self.fatal_conflicts.append(
                    MergeConflict(
                        dst=path,
                        src_a=os.path.join(src_a_root, src_a_relpath),
                        src_b=os.path.join("<projection>", path),
                    )
                )


class DestinationMergeVisitor(BaseDirectoryVisitor):
    """DestinatinoMergeVisitor takes a SourceMergeVisitor and:

    a. registers additional conflicts when merging to the destination prefix
    b. removes redundant mkdir operations when directories already exist in the destination prefix.

    This also makes sure that symlinked directories in the target prefix will never be merged with
    directories in the sources directories.
    """

    def __init__(self, source_merge_visitor: SourceMergeVisitor):
        self.src = source_merge_visitor

    def before_visit_dir(self, root: str, rel_path: str, depth: int) -> bool:
        # If destination dir is a file in a src dir, add a conflict,
        # and don't traverse deeper
        if rel_path in self.src.files:
            src_a_root, src_a_relpath = self.src.files[rel_path]
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )
            return False

        # If destination dir was also a src dir, remove the mkdir
        # action, and traverse deeper.
        if rel_path in self.src.directories:
            del self.src.directories[rel_path]
            return True

        # If the destination dir does not appear in the src dir,
        # don't descend into it.
        return False

    def before_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """
        Symlinked directories in the destination prefix should
        be seen as files; we should not accidentally merge
        source dir with a symlinked dest dir.
        """
        # Always conflict
        if rel_path in self.src.directories:
            src_a_root, src_a_relpath = self.src.directories[rel_path]
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

        if rel_path in self.src.files:
            src_a_root, src_a_relpath = self.src.files[rel_path]
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

        # Never descend into symlinked target dirs.
        return False

    def visit_file(self, root: str, rel_path: str, depth: int) -> None:
        # Can't merge a file if target already exists
        if rel_path in self.src.directories:
            src_a_root, src_a_relpath = self.src.directories[rel_path]
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

        elif rel_path in self.src.files:
            src_a_root, src_a_relpath = self.src.files[rel_path]
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

    def visit_symlinked_file(self, root: str, rel_path: str, depth: int) -> None:
        # Treat symlinked files as ordinary files (without "dereferencing")
        self.visit_file(root, rel_path, depth)


class LinkTree:
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directries are never
    symlinked to, to prevent the source directory from ever being
    modified.
    """

    def __init__(self, source_root):
        if not os.path.exists(source_root):
            raise IOError("No such file or directory: '%s'", source_root)

        self._root = source_root

    def find_conflict(self, dest_root, ignore=None, ignore_file_conflicts=False):
        """Returns the first file in dest that conflicts with src"""
        ignore = ignore or (lambda x: False)
        conflicts = self.find_dir_conflicts(dest_root, ignore)

        if not ignore_file_conflicts:
            conflicts.extend(
                dst
                for src, dst in self.get_file_map(dest_root, ignore).items()
                if os.path.exists(dst)
            )

        if conflicts:
            return conflicts[0]

    def find_dir_conflicts(self, dest_root, ignore):
        conflicts = []
        kwargs = {"follow_nonexisting": False, "ignore": ignore}
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    conflicts.append("File blocks directory: %s" % dest)
            elif os.path.exists(dest) and os.path.isdir(dest):
                conflicts.append("Directory blocks directory: %s" % dest)
        return conflicts

    def get_file_map(self, dest_root, ignore):
        merge_map = {}
        kwargs = {"follow_nonexisting": True, "ignore": ignore}
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if not os.path.isdir(src):
                merge_map[src] = dest
        return merge_map

    def merge_directories(self, dest_root, ignore):
        for src, dest in traverse_tree(self._root, dest_root, ignore=ignore):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    mkdirp(dest)
                    continue

                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # mark empty directories so they aren't removed on unmerge.
                if not os.listdir(dest):
                    marker = os.path.join(dest, empty_file_name)
                    touch(marker)

    def unmerge_directories(self, dest_root, ignore):
        for src, dest in traverse_tree(self._root, dest_root, ignore=ignore, order="post"):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    continue
                elif not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # remove directory if it is empty.
                if not os.listdir(dest):
                    shutil.rmtree(dest, ignore_errors=True)

                # remove empty dir marker if present.
                marker = os.path.join(dest, empty_file_name)
                if os.path.exists(marker):
                    os.remove(marker)

    def merge(self, dest_root, ignore_conflicts=False, ignore=None, link=symlink, relative=False):
        """Link all files in src into dest, creating directories
           if necessary.

        Keyword Args:

        ignore_conflicts (bool): if True, do not break when the target exists;
            return a list of files that could not be linked

        ignore (callable): callable that returns True if a file is to be
            ignored in the merge (by default ignore nothing)

        link (callable): function to create links with (defaults to llnl.util.symlink)

        relative (bool): create all symlinks relative to the target
            (default False)

        """
        if ignore is None:
            ignore = lambda x: False

        conflict = self.find_conflict(
            dest_root, ignore=ignore, ignore_file_conflicts=ignore_conflicts
        )
        if conflict:
            raise SingleMergeConflictError(conflict)

        self.merge_directories(dest_root, ignore)
        existing = []
        for src, dst in self.get_file_map(dest_root, ignore).items():
            if os.path.exists(dst):
                existing.append(dst)
            elif relative:
                abs_src = os.path.abspath(src)
                dst_dir = os.path.dirname(os.path.abspath(dst))
                rel = os.path.relpath(abs_src, dst_dir)
                link(rel, dst)
            else:
                link(src, dst)

        for c in existing:
            tty.warn("Could not merge: %s" % c)

    def unmerge(self, dest_root, ignore=None, remove_file=remove_link):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.
        """
        if ignore is None:
            ignore = lambda x: False

        for src, dst in self.get_file_map(dest_root, ignore).items():
            remove_file(src, dst)
        self.unmerge_directories(dest_root, ignore)


class MergeConflictError(Exception):
    pass


class ConflictingSpecsError(MergeConflictError):
    def __init__(self, spec_1, spec_2):
        super().__init__(spec_1, spec_2)


class SingleMergeConflictError(MergeConflictError):
    def __init__(self, path):
        super().__init__("Package merge blocked by file: %s" % path)


class MergeConflictSummary(MergeConflictError):
    def __init__(self, conflicts):
        """
        A human-readable summary of file system view merge conflicts (showing only the
        first 3 issues.)
        """
        msg = "{0} fatal error(s) when merging prefixes:".format(len(conflicts))
        # show the first 3 merge conflicts.
        for conflict in conflicts[:3]:
            msg += "\n    `{0}` and `{1}` both project to `{2}`".format(
                conflict.src_a, conflict.src_b, conflict.dst
            )
        super().__init__(msg)
