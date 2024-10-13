# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools as ft
import itertools
import os
import re
import shutil
import stat
import sys
from typing import Callable, Dict, Optional

from llnl.string import comma_or
from llnl.util import tty
from llnl.util.filesystem import (
    mkdirp,
    remove_dead_links,
    remove_empty_directories,
    visit_directory_tree,
)
from llnl.util.lang import index_by, match_predicate
from llnl.util.link_tree import (
    ConflictingSpecsError,
    DestinationMergeVisitor,
    LinkTree,
    MergeConflictSummary,
    SingleMergeConflictError,
    SourceMergeVisitor,
)
from llnl.util.symlink import symlink
from llnl.util.tty.color import colorize

import spack.config
import spack.paths
import spack.projections
import spack.relocate
import spack.schema.projections
import spack.spec
import spack.store
import spack.util.spack_json as s_json
import spack.util.spack_yaml as s_yaml
from spack.error import SpackError
from spack.hooks import sbang

__all__ = ["FilesystemView", "YamlFilesystemView"]


_projections_path = ".spack/projections.yaml"


LinkCallbackType = Callable[[str, str, "FilesystemView", Optional["spack.spec.Spec"]], None]


def view_symlink(src: str, dst: str, *args, **kwargs) -> None:
    symlink(src, dst)


def view_hardlink(src: str, dst: str, *args, **kwargs) -> None:
    os.link(src, dst)


def view_copy(
    src: str, dst: str, view: "FilesystemView", spec: Optional["spack.spec.Spec"] = None
) -> None:
    """
    Copy a file from src to dst.

    Use spec and view to generate relocations
    """
    shutil.copy2(src, dst, follow_symlinks=False)

    # No need to relocate if no metadata or external.
    if not spec or spec.external:
        return

    # Order of this dict is somewhat irrelevant
    prefix_to_projection = {
        s.prefix: view.get_projection_for_spec(s)
        for s in spec.traverse(root=True, order="breadth")
        if not s.external
    }

    src_stat = os.lstat(src)

    # TODO: change this into a bulk operation instead of a per-file operation

    if stat.S_ISLNK(src_stat.st_mode):
        spack.relocate.relocate_links(links=[dst], prefix_to_prefix=prefix_to_projection)
    elif spack.relocate.is_binary(dst):
        spack.relocate.relocate_text_bin(binaries=[dst], prefixes=prefix_to_projection)
    else:
        prefix_to_projection[spack.store.STORE.layout.root] = view._root

        # This is vestigial code for the *old* location of sbang.
        prefix_to_projection[f"#!/bin/bash {spack.paths.spack_root}/bin/sbang"] = (
            sbang.sbang_shebang_line()
        )

        spack.relocate.relocate_text(files=[dst], prefixes=prefix_to_projection)

    # The os module on Windows does not have a chown function.
    if sys.platform != "win32":
        try:
            os.chown(dst, src_stat.st_uid, src_stat.st_gid)
        except OSError:
            tty.debug(f"Can't change the permissions for {dst}")


#: supported string values for `link_type` in an env, mapped to canonical values
_LINK_TYPES = {
    "hardlink": "hardlink",
    "hard": "hardlink",
    "copy": "copy",
    "relocate": "copy",
    "add": "symlink",
    "symlink": "symlink",
    "soft": "symlink",
}

_VALID_LINK_TYPES = sorted(set(_LINK_TYPES.values()))


def canonicalize_link_type(link_type: str) -> str:
    """Return canonical"""
    canonical = _LINK_TYPES.get(link_type)
    if not canonical:
        raise ValueError(
            f"Invalid link type: '{link_type}. Must be one of {comma_or(_VALID_LINK_TYPES)}'"
        )
    return canonical


def function_for_link_type(link_type: str) -> LinkCallbackType:
    link_type = canonicalize_link_type(link_type)
    if link_type == "hardlink":
        return view_hardlink
    elif link_type == "symlink":
        return view_symlink
    elif link_type == "copy":
        return view_copy

    assert False, "invalid link type"  # need mypy Literal values


class FilesystemView:
    """
    Governs a filesystem view that is located at certain root-directory.

    Packages are linked from their install directories into a common file
    hierachy.

    In distributed filesystems, loading each installed package seperately
    can lead to slow-downs due to too many directories being traversed.
    This can be circumvented by loading all needed modules into a common
    directory structure.
    """

    def __init__(
        self,
        root: str,
        layout: "spack.directory_layout.DirectoryLayout",
        *,
        projections: Optional[Dict] = None,
        ignore_conflicts: bool = False,
        verbose: bool = False,
        link_type: str = "symlink",
    ):
        """
        Initialize a filesystem view under the given `root` directory with
        corresponding directory `layout`.

        Files are linked by method `link` (llnl.util.symlink by default).
        """
        self._root = root
        self.layout = layout
        self.projections = {} if projections is None else projections

        self.ignore_conflicts = ignore_conflicts
        self.verbose = verbose

        # Setup link function to include view
        self.link_type = link_type
        self.link = ft.partial(function_for_link_type(link_type), view=self)

    def add_specs(self, *specs, **kwargs):
        """
        Add given specs to view.

        Should accept `with_dependencies` as keyword argument (default
        True) to indicate wether or not dependencies should be activated as
        well.

        Should except an `exclude` keyword argument containing a list of
        regexps that filter out matching spec names.

        This method should make use of `activate_standalone`.
        """
        raise NotImplementedError

    def add_standalone(self, spec):
        """
        Add (link) a standalone package into this view.
        """
        raise NotImplementedError

    def check_added(self, spec):
        """
        Check if the given concrete spec is active in this view.
        """
        raise NotImplementedError

    def remove_specs(self, *specs, **kwargs):
        """
        Removes given specs from view.

        Should accept `with_dependencies` as keyword argument (default
        True) to indicate wether or not dependencies should be deactivated
        as well.

        Should accept `with_dependents` as keyword argument (default True)
        to indicate wether or not dependents on the deactivated specs
        should be removed as well.

        Should except an `exclude` keyword argument containing a list of
        regexps that filter out matching spec names.

        This method should make use of `deactivate_standalone`.
        """
        raise NotImplementedError

    def remove_standalone(self, spec):
        """
        Remove (unlink) a standalone package from this view.
        """
        raise NotImplementedError

    def get_projection_for_spec(self, spec):
        """
        Get the projection in this view for a spec.
        """
        raise NotImplementedError

    def get_all_specs(self):
        """
        Get all specs currently active in this view.
        """
        raise NotImplementedError

    def get_spec(self, spec):
        """
        Return the actual spec linked in this view (i.e. do not look it up
        in the database by name).

        `spec` can be a name or a spec from which the name is extracted.

        As there can only be a single version active for any spec the name
        is enough to identify the spec in the view.

        If no spec is present, returns None.
        """
        raise NotImplementedError

    def print_status(self, *specs, **kwargs):
        """
        Print a short summary about the given specs, detailing whether..
            * ..they are active in the view.
            * ..they are active but the activated version differs.
            * ..they are not activte in the view.

        Takes `with_dependencies` keyword argument so that the status of
        dependencies is printed as well.
        """
        raise NotImplementedError


class YamlFilesystemView(FilesystemView):
    """
    Filesystem view to work with a yaml based directory layout.
    """

    def __init__(
        self,
        root: str,
        layout: "spack.directory_layout.DirectoryLayout",
        *,
        projections: Optional[Dict] = None,
        ignore_conflicts: bool = False,
        verbose: bool = False,
        link_type: str = "symlink",
    ):
        super().__init__(
            root,
            layout,
            projections=projections,
            ignore_conflicts=ignore_conflicts,
            verbose=verbose,
            link_type=link_type,
        )

        # Super class gets projections from the kwargs
        # YAML specific to get projections from YAML file
        self.projections_path = os.path.join(self._root, _projections_path)
        if not self.projections:
            # Read projections file from view
            self.projections = self.read_projections()
        elif not os.path.exists(self.projections_path):
            # Write projections file to new view
            self.write_projections()
        else:
            # Ensure projections are the same from each source
            # Read projections file from view
            if self.projections != self.read_projections():
                raise ConflictingProjectionsError(
                    f"View at {self._root} has projections file"
                    " which does not match projections passed manually."
                )

        self._croot = colorize_root(self._root) + " "

    def write_projections(self):
        if self.projections:
            mkdirp(os.path.dirname(self.projections_path))
            with open(self.projections_path, "w") as f:
                f.write(s_yaml.dump_config({"projections": self.projections}))

    def read_projections(self):
        if os.path.exists(self.projections_path):
            with open(self.projections_path, "r") as f:
                projections_data = s_yaml.load(f)
                spack.config.validate(projections_data, spack.schema.projections.schema)
                return projections_data["projections"]
        else:
            return {}

    def add_specs(self, *specs, **kwargs):
        assert all((s.concrete for s in specs))
        specs = set(specs)

        if kwargs.get("with_dependencies", True):
            specs.update(get_dependencies(specs))

        if kwargs.get("exclude", None):
            specs = set(filter_exclude(specs, kwargs["exclude"]))

        conflicts = self.get_conflicts(*specs)

        if conflicts:
            for s, v in conflicts:
                self.print_conflict(v, s)
            return

        for s in specs:
            self.add_standalone(s)

    def add_standalone(self, spec):
        if spec.external:
            tty.warn(f"{self._croot}Skipping external package: {colorize_spec(spec)}")
            return True

        if self.check_added(spec):
            tty.warn(f"{self._croot}Skipping already linked package: {colorize_spec(spec)}")
            return True

        self.merge(spec)

        self.link_meta_folder(spec)

        if self.verbose:
            tty.info(f"{self._croot}Linked package: {colorize_spec(spec)}")
        return True

    def merge(self, spec, ignore=None):
        pkg = spec.package
        view_source = pkg.view_source()
        view_dst = pkg.view_destination(self)

        tree = LinkTree(view_source)

        ignore = ignore or (lambda f: False)
        ignore_file = match_predicate(self.layout.hidden_file_regexes, ignore)

        # check for dir conflicts
        conflicts = tree.find_dir_conflicts(view_dst, ignore_file)

        merge_map = tree.get_file_map(view_dst, ignore_file)
        if not self.ignore_conflicts:
            conflicts.extend(pkg.view_file_conflicts(self, merge_map))

        if conflicts:
            raise SingleMergeConflictError(conflicts[0])

        # merge directories with the tree
        tree.merge_directories(view_dst, ignore_file)

        pkg.add_files_to_view(self, merge_map)

    def unmerge(self, spec, ignore=None):
        pkg = spec.package
        view_source = pkg.view_source()
        view_dst = pkg.view_destination(self)

        tree = LinkTree(view_source)

        ignore = ignore or (lambda f: False)
        ignore_file = match_predicate(self.layout.hidden_file_regexes, ignore)

        merge_map = tree.get_file_map(view_dst, ignore_file)
        pkg.remove_files_from_view(self, merge_map)

        # now unmerge the directory tree
        tree.unmerge_directories(view_dst, ignore_file)

    def remove_files(self, files):
        def needs_file(spec, file):
            # convert the file we want to remove to a source in this spec
            projection = self.get_projection_for_spec(spec)
            relative_path = os.path.relpath(file, projection)
            test_path = os.path.join(spec.prefix, relative_path)

            # check if this spec owns a file of that name (through the
            # manifest in the metadata dir, which we have in the view).
            manifest_file = os.path.join(
                self.get_path_meta_folder(spec), spack.store.STORE.layout.manifest_file_name
            )
            try:
                with open(manifest_file, "r") as f:
                    manifest = s_json.load(f)
            except (OSError, IOError):
                # if we can't load it, assume it doesn't know about the file.
                manifest = {}
            return test_path in manifest

        specs = self.get_all_specs()

        for file in files:
            if not os.path.lexists(file):
                tty.warn(f"Tried to remove {file} which does not exist")
                continue

            # remove if file is not owned by any other package in the view
            # This will only be false if two packages are merged into a prefix
            # and have a conflicting file

            # check all specs for whether they own the file. That include the spec
            # we are currently removing, as we remove files before unlinking the
            # metadata directory.
            if len([s for s in specs if needs_file(s, file)]) <= 1:
                tty.debug(f"Removing file {file}")
                os.remove(file)

    def check_added(self, spec):
        assert spec.concrete
        return spec == self.get_spec(spec)

    def remove_specs(self, *specs, **kwargs):
        assert all((s.concrete for s in specs))
        with_dependents = kwargs.get("with_dependents", True)
        with_dependencies = kwargs.get("with_dependencies", False)

        # caller can pass this in, as get_all_specs() is expensive
        all_specs = kwargs.get("all_specs", None) or set(self.get_all_specs())

        specs = set(specs)

        if with_dependencies:
            specs = get_dependencies(specs)

        if kwargs.get("exclude", None):
            specs = set(filter_exclude(specs, kwargs["exclude"]))

        to_deactivate = specs
        to_keep = all_specs - to_deactivate

        dependents = find_dependents(to_keep, to_deactivate)

        if with_dependents:
            # remove all packages depending on the ones to remove
            if len(dependents) > 0:
                tty.warn(
                    self._croot
                    + "The following dependents will be removed: %s"
                    % ", ".join((s.name for s in dependents))
                )
                to_deactivate.update(dependents)
        elif len(dependents) > 0:
            tty.warn(
                self._croot
                + "The following packages will be unusable: %s"
                % ", ".join((s.name for s in dependents))
            )

        # Determine the order that packages should be removed from the view;
        # dependents come before their dependencies.
        to_deactivate_sorted = list()
        depmap = dict()
        for spec in to_deactivate:
            depmap[spec] = set(d for d in spec.traverse(root=False) if d in to_deactivate)

        while depmap:
            for spec in [s for s, d in depmap.items() if not d]:
                to_deactivate_sorted.append(spec)
                for s in depmap.keys():
                    depmap[s].discard(spec)
                depmap.pop(spec)
        to_deactivate_sorted.reverse()

        # Ensure that the sorted list contains all the packages
        assert set(to_deactivate_sorted) == to_deactivate

        # Remove the packages from the view
        for spec in to_deactivate_sorted:
            self.remove_standalone(spec)

        self._purge_empty_directories()

    def remove_standalone(self, spec):
        """
        Remove (unlink) a standalone package from this view.
        """
        if not self.check_added(spec):
            tty.warn(f"{self._croot}Skipping package not linked in view: {spec.name}")
            return

        self.unmerge(spec)
        self.unlink_meta_folder(spec)

        if self.verbose:
            tty.info(f"{self._croot}Removed package: {colorize_spec(spec)}")

    def get_projection_for_spec(self, spec):
        """
        Return the projection for a spec in this view.

        Relies on the ordering of projections to avoid ambiguity.
        """
        spec = spack.spec.Spec(spec)
        locator_spec = spec

        if spec.package.extendee_spec:
            locator_spec = spec.package.extendee_spec

        proj = spack.projections.get_projection(self.projections, locator_spec)
        if proj:
            return os.path.join(self._root, locator_spec.format_path(proj))
        return self._root

    def get_all_specs(self):
        md_dirs = []
        for root, dirs, files in os.walk(self._root):
            if spack.store.STORE.layout.metadata_dir in dirs:
                md_dirs.append(os.path.join(root, spack.store.STORE.layout.metadata_dir))

        specs = []
        for md_dir in md_dirs:
            if os.path.exists(md_dir):
                for name_dir in os.listdir(md_dir):
                    filename = os.path.join(
                        md_dir, name_dir, spack.store.STORE.layout.spec_file_name
                    )
                    spec = get_spec_from_file(filename)
                    if spec:
                        specs.append(spec)
        return specs

    def get_conflicts(self, *specs):
        """
        Return list of tuples (<spec>, <spec in view>) where the spec
        active in the view differs from the one to be activated.
        """
        in_view = map(self.get_spec, specs)
        return [(s, v) for s, v in zip(specs, in_view) if v is not None and s != v]

    def get_path_meta_folder(self, spec):
        "Get path to meta folder for either spec or spec name."
        return os.path.join(
            self.get_projection_for_spec(spec),
            spack.store.STORE.layout.metadata_dir,
            getattr(spec, "name", spec),
        )

    def get_spec(self, spec):
        dotspack = self.get_path_meta_folder(spec)
        filename = os.path.join(dotspack, spack.store.STORE.layout.spec_file_name)

        return get_spec_from_file(filename)

    def link_meta_folder(self, spec):
        src = spack.store.STORE.layout.metadata_path(spec)
        tgt = self.get_path_meta_folder(spec)

        tree = LinkTree(src)
        # there should be no conflicts when linking the meta folder
        tree.merge(tgt, link=self.link)

    def print_conflict(self, spec_active, spec_specified, level="error"):
        "Singular print function for spec conflicts."
        cprint = getattr(tty, level)
        color = sys.stdout.isatty()
        linked = tty.color.colorize("   (@gLinked@.)", color=color)
        specified = tty.color.colorize("(@rSpecified@.)", color=color)
        cprint(
            f"{self._croot}Package conflict detected:\n"
            f"{linked} {colorize_spec(spec_active)}\n"
            f"{specified} {colorize_spec(spec_specified)}"
        )

    def print_status(self, *specs, **kwargs):
        if kwargs.get("with_dependencies", False):
            specs = set(get_dependencies(specs))

        specs = sorted(specs, key=lambda s: s.name)
        in_view = list(map(self.get_spec, specs))

        for s, v in zip(specs, in_view):
            if not v:
                tty.error(f"{self._croot}Package not linked: {s.name}")
            elif s != v:
                self.print_conflict(v, s, level="warn")

        in_view = list(filter(None, in_view))

        if len(specs) > 0:
            tty.msg(f"Packages linked in {self._croot[:-1]}:")

            # Make a dict with specs keyed by architecture and compiler.
            index = index_by(specs, ("architecture", "compiler"))

            # Traverse the index and print out each package
            for i, (architecture, compiler) in enumerate(sorted(index)):
                if i > 0:
                    print()

                header = (
                    f"{spack.spec.ARCHITECTURE_COLOR}{{{architecture}}} "
                    f"/ {spack.spec.COMPILER_COLOR}{{{compiler}}}"
                )
                tty.hline(colorize(header), char="-")

                specs = index[(architecture, compiler)]
                specs.sort()

                abbreviated = [
                    s.cformat("{name}{@version}{%compiler}{compiler_flags}{variants}")
                    for s in specs
                ]

                # Print one spec per line along with prefix path
                width = max(len(s) for s in abbreviated)
                width += 2
                format = "    %%-%ds%%s" % width

                for abbrv, s in zip(abbreviated, specs):
                    prefix = ""
                    if self.verbose:
                        prefix = colorize("@K{%s}" % s.dag_hash(7))
                    print(prefix + (format % (abbrv, self.get_projection_for_spec(s))))
        else:
            tty.warn(self._croot + "No packages found.")

    def _purge_empty_directories(self):
        remove_empty_directories(self._root)

    def _purge_broken_links(self):
        remove_dead_links(self._root)

    def clean(self):
        self._purge_broken_links()
        self._purge_empty_directories()

    def unlink_meta_folder(self, spec):
        path = self.get_path_meta_folder(spec)
        assert os.path.exists(path)
        shutil.rmtree(path)


class SimpleFilesystemView(FilesystemView):
    """A simple and partial implementation of FilesystemView focused on performance and immutable
    views, where specs cannot be removed after they were added."""

    def _sanity_check_view_projection(self, specs):
        """A very common issue is that we end up with two specs of the same package, that project
        to the same prefix. We want to catch that as early as possible and give a sensible error to
        the user. Here we use the metadata dir (.spack) projection as a quick test to see whether
        two specs in the view are going to clash. The metadata dir is used because it's always
        added by Spack with identical files, so a guaranteed clash that's easily verified."""
        seen = {}
        for current_spec in specs:
            metadata_dir = self.relative_metadata_dir_for_spec(current_spec)
            conflicting_spec = seen.get(metadata_dir)
            if conflicting_spec:
                raise ConflictingSpecsError(current_spec, conflicting_spec)
            seen[metadata_dir] = current_spec

    def add_specs(self, *specs: spack.spec.Spec) -> None:
        """Link a root-to-leaf topologically ordered list of specs into the view."""
        assert all((s.concrete for s in specs))
        if len(specs) == 0:
            return

        # Drop externals
        specs = [s for s in specs if not s.external]

        self._sanity_check_view_projection(specs)

        # Ignore spack meta data folder.
        def skip_list(file):
            return os.path.basename(file) == spack.store.STORE.layout.metadata_dir

        visitor = SourceMergeVisitor(ignore=skip_list)

        # Gather all the directories to be made and files to be linked
        for spec in specs:
            src_prefix = spec.package.view_source()
            visitor.set_projection(self.get_relative_projection_for_spec(spec))
            visit_directory_tree(src_prefix, visitor)

        # Check for conflicts in destination dir.
        visit_directory_tree(self._root, DestinationMergeVisitor(visitor))

        # Throw on fatal dir-file conflicts.
        if visitor.fatal_conflicts:
            raise MergeConflictSummary(visitor.fatal_conflicts)

        # Inform about file-file conflicts.
        if visitor.file_conflicts:
            if self.ignore_conflicts:
                tty.debug(f"{len(visitor.file_conflicts)} file conflicts")
            else:
                raise MergeConflictSummary(visitor.file_conflicts)

        tty.debug(f"Creating {len(visitor.directories)} dirs and {len(visitor.files)} links")

        # Make the directory structure
        for dst in visitor.directories:
            os.mkdir(os.path.join(self._root, dst))

        # Link the files using a "merge map": full src => full dst
        merge_map_per_prefix = self._source_merge_visitor_to_merge_map(visitor)
        for spec in specs:
            merge_map = merge_map_per_prefix.get(spec.package.view_source(), None)
            if not merge_map:
                # Not every spec may have files to contribute.
                continue
            spec.package.add_files_to_view(self, merge_map, skip_if_exists=False)

        # Finally create the metadata dirs.
        self.link_metadata(specs)

    def _source_merge_visitor_to_merge_map(self, visitor: SourceMergeVisitor):
        # For compatibility with add_files_to_view, we have to create a
        # merge_map of the form join(src_root, src_rel) => join(dst_root, dst_rel),
        # but our visitor.files format is dst_rel => (src_root, src_rel).
        # We exploit that visitor.files is an ordered dict, and files per source
        # prefix are contiguous.
        source_root = lambda item: item[1][0]
        per_source = itertools.groupby(visitor.files.items(), key=source_root)
        return {
            src_root: {
                os.path.join(src_root, src_rel): os.path.join(self._root, dst_rel)
                for dst_rel, (_, src_rel) in group
            }
            for src_root, group in per_source
        }

    def relative_metadata_dir_for_spec(self, spec):
        return os.path.join(
            self.get_relative_projection_for_spec(spec),
            spack.store.STORE.layout.metadata_dir,
            spec.name,
        )

    def link_metadata(self, specs):
        metadata_visitor = SourceMergeVisitor()

        for spec in specs:
            src_prefix = os.path.join(
                spec.package.view_source(), spack.store.STORE.layout.metadata_dir
            )
            proj = self.relative_metadata_dir_for_spec(spec)
            metadata_visitor.set_projection(proj)
            visit_directory_tree(src_prefix, metadata_visitor)

        # Check for conflicts in destination dir.
        visit_directory_tree(self._root, DestinationMergeVisitor(metadata_visitor))

        # Throw on dir-file conflicts -- unlikely, but who knows.
        if metadata_visitor.fatal_conflicts:
            raise MergeConflictSummary(metadata_visitor.fatal_conflicts)

        # We are strict here for historical reasons
        if metadata_visitor.file_conflicts:
            raise MergeConflictSummary(metadata_visitor.file_conflicts)

        for dst in metadata_visitor.directories:
            os.mkdir(os.path.join(self._root, dst))

        for dst_relpath, (src_root, src_relpath) in metadata_visitor.files.items():
            self.link(os.path.join(src_root, src_relpath), os.path.join(self._root, dst_relpath))

    def get_relative_projection_for_spec(self, spec):
        # Extensions are placed by their extendee, not by their own spec
        if spec.package.extendee_spec:
            spec = spec.package.extendee_spec

        p = spack.projections.get_projection(self.projections, spec)
        return spec.format_path(p) if p else ""

    def get_projection_for_spec(self, spec):
        """
        Return the projection for a spec in this view.

        Relies on the ordering of projections to avoid ambiguity.
        """
        spec = spack.spec.Spec(spec)

        if spec.package.extendee_spec:
            spec = spec.package.extendee_spec

        proj = spack.projections.get_projection(self.projections, spec)
        if proj:
            return os.path.join(self._root, spec.format_path(proj))
        return self._root


#####################
# utility functions #
#####################
def get_spec_from_file(filename):
    try:
        with open(filename, "r") as f:
            return spack.spec.Spec.from_yaml(f)
    except IOError:
        return None


def colorize_root(root):
    colorize = ft.partial(tty.color.colorize, color=sys.stdout.isatty())
    pre, post = map(colorize, "@M[@. @M]@.".split())
    return "".join([pre, root, post])


def colorize_spec(spec):
    "Colorize spec output if in TTY."
    if sys.stdout.isatty():
        return spec.cshort_spec
    else:
        return spec.short_spec


def find_dependents(all_specs, providers, deptype="run"):
    """
    Return a set containing all those specs from all_specs that depend on
    providers at the given dependency type.
    """
    dependents = set()
    for s in all_specs:
        for dep in s.traverse(deptype=deptype):
            if dep in providers:
                dependents.add(s)
    return dependents


def filter_exclude(specs, exclude):
    "Filter specs given sequence of exclude regex"
    to_exclude = [re.compile(e) for e in exclude]

    def keep(spec):
        for e in to_exclude:
            if e.match(spec.name):
                return False
        return True

    return filter(keep, specs)


def get_dependencies(specs):
    "Get set of dependencies (includes specs)"
    retval = set()
    set(map(retval.update, (set(s.traverse()) for s in specs)))
    return retval


class ConflictingProjectionsError(SpackError):
    """Raised when a view has a projections file and is given one manually."""
