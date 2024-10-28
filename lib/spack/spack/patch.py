# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os
import os.path
import pathlib
import sys
from typing import Any, Dict, Optional, Tuple, Type, Union

import llnl.util.filesystem
from llnl.url import allowed_archive

import spack
import spack.error
import spack.fetch_strategy
import spack.mirror
import spack.repo
import spack.stage
import spack.util.spack_json as sjson
from spack.util.crypto import Checker, checksum
from spack.util.executable import which, which_string


def apply_patch(
    stage: "spack.stage.Stage",
    patch_path: str,
    level: int = 1,
    working_dir: str = ".",
    reverse: bool = False,
) -> None:
    """Apply the patch at patch_path to code in the stage.

    Args:
        stage: stage with code that will be patched
        patch_path: filesystem location for the patch to apply
        level: patch level
        working_dir: relative path *within* the stage to change to
        reverse: reverse the patch
    """
    git_utils_path = os.environ.get("PATH", "")
    if sys.platform == "win32":
        git = which_string("git")
        if git:
            git = pathlib.Path(git)
            git_root = git.parent.parent
            git_root = git_root / "usr" / "bin"
            git_utils_path = os.pathsep.join([str(git_root), git_utils_path])

    args = ["-s", "-p", str(level), "-i", patch_path, "-d", working_dir]
    if reverse:
        args.append("-R")

    # TODO: Decouple Spack's patch support on Windows from Git
    # for Windows, and instead have Spack directly fetch, install, and
    # utilize that patch.
    # Note for future developers: The GNU port of patch to windows
    # has issues handling CRLF line endings unless the --binary
    # flag is passed.
    patch = which("patch", required=True, path=git_utils_path)
    with llnl.util.filesystem.working_dir(stage.source_path):
        patch(*args)


PatchPackageType = Union["spack.package_base.PackageBase", Type["spack.package_base.PackageBase"]]


class Patch:
    """Base class for patches.

    The owning package is not necessarily the package to apply the patch
    to -- in the case where a dependent package patches its dependency,
    it is the dependent's fullname.
    """

    sha256: str

    def __init__(
        self,
        pkg: PatchPackageType,
        path_or_url: str,
        level: int,
        working_dir: str,
        reverse: bool = False,
    ) -> None:
        """Initialize a new Patch instance.

        Args:
            pkg: the package that owns the patch
            path_or_url: the relative path or URL to a patch file
            level: patch level
            working_dir: relative path *within* the stage to change to
            reverse: reverse the patch
        """
        # validate level (must be an integer >= 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

        # Attributes shared by all patch subclasses
        self.owner = pkg.fullname
        self.path_or_url = path_or_url  # needed for debug output
        self.path: Optional[str] = None  # must be set before apply()
        self.level = level
        self.working_dir = working_dir
        self.reverse = reverse

    def apply(self, stage: "spack.stage.Stage") -> None:
        """Apply a patch to source in a stage.

        Args:
            stage: stage where source code lives
        """
        if not self.path or not os.path.isfile(self.path):
            raise spack.error.NoSuchPatchError(f"No such patch: {self.path}")

        apply_patch(stage, self.path, self.level, self.working_dir, self.reverse)

    # TODO: Use TypedDict once Spack supports Python 3.8+ only
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary representation of the patch.

        Returns:
            A dictionary representation.
        """
        return {
            "owner": self.owner,
            "sha256": self.sha256,
            "level": self.level,
            "working_dir": self.working_dir,
            "reverse": self.reverse,
        }

    def __eq__(self, other: object) -> bool:
        """Equality check.

        Args:
            other: another patch

        Returns:
            True if both patches have the same checksum, else False
        """
        if not isinstance(other, Patch):
            return NotImplemented
        return self.sha256 == other.sha256

    def __hash__(self) -> int:
        """Unique hash.

        Returns:
            A unique hash based on the sha256.
        """
        return hash(self.sha256)


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository."""

    _sha256: Optional[str] = None

    def __init__(
        self,
        pkg: PatchPackageType,
        relative_path: str,
        level: int,
        working_dir: str,
        reverse: bool = False,
        ordering_key: Optional[Tuple[str, int]] = None,
    ) -> None:
        """Initialize a new FilePatch instance.

        Args:
            pkg: the class object for the package that owns the patch
            relative_path: path to patch, relative to the repository directory for a package.
            level: level to pass to patch command
            working_dir: path within the source directory where patch should be applied
            reverse: reverse the patch
            ordering_key: key used to ensure patches are applied in a consistent order
        """
        self.relative_path = relative_path

        # patches may be defined by relative paths to parent classes
        # search mro to look for the file
        abs_path: Optional[str] = None
        # At different times we call FilePatch on instances and classes
        pkg_cls = pkg if isinstance(pkg, type) else pkg.__class__
        for cls in pkg_cls.__mro__:  # type: ignore
            if not hasattr(cls, "module"):
                # We've gone too far up the MRO
                break

            # Cannot use pkg.package_dir because it's a property and we have
            # classes, not instances.
            pkg_dir = os.path.abspath(os.path.dirname(cls.module.__file__))
            path = os.path.join(pkg_dir, self.relative_path)
            if os.path.exists(path):
                abs_path = path
                break

        if abs_path is None:
            msg = "FilePatch: Patch file %s for " % relative_path
            msg += "package %s.%s does not exist." % (pkg.namespace, pkg.name)
            raise ValueError(msg)

        super().__init__(pkg, abs_path, level, working_dir, reverse)
        self.path = abs_path
        self.ordering_key = ordering_key

    @property
    def sha256(self) -> str:
        """Get the patch checksum.

        Returns:
            The sha256 of the patch file.
        """
        if self._sha256 is None and self.path is not None:
            self._sha256 = checksum(hashlib.sha256, self.path)
        assert isinstance(self._sha256, str)
        return self._sha256

    @sha256.setter
    def sha256(self, value: str) -> None:
        """Set the patch checksum.

        Args:
            value: the sha256
        """
        self._sha256 = value

    def to_dict(self) -> Dict[str, Any]:
        """Dictionary representation of the patch.

        Returns:
            A dictionary representation.
        """
        data = super().to_dict()
        data["relative_path"] = self.relative_path
        return data


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL."""

    def __init__(
        self,
        pkg: PatchPackageType,
        url: str,
        level: int = 1,
        *,
        working_dir: str = ".",
        reverse: bool = False,
        sha256: str,  # This is required for UrlPatch
        ordering_key: Optional[Tuple[str, int]] = None,
        archive_sha256: Optional[str] = None,
    ) -> None:
        """Initialize a new UrlPatch instance.

        Arguments:
            pkg: the package that owns the patch
            url: URL where the patch can be fetched
            level: level to pass to patch command
            working_dir: path within the source directory where patch should be applied
            reverse: reverse the patch
            ordering_key: key used to ensure patches are applied in a consistent order
            sha256: sha256 sum of the patch, used to verify the patch
            archive_sha256: sha256 sum of the *archive*, if the patch is compressed
                (only required for compressed URL patches)
        """
        super().__init__(pkg, url, level, working_dir, reverse)

        self.url = url
        self._stage: Optional["spack.stage.Stage"] = None

        self.ordering_key = ordering_key

        if allowed_archive(self.url) and not archive_sha256:
            raise spack.error.PatchDirectiveError(
                "Compressed patches require 'archive_sha256' "
                "and patch 'sha256' attributes: %s" % self.url
            )
        self.archive_sha256 = archive_sha256

        if not sha256:
            raise spack.error.PatchDirectiveError("URL patches require a sha256 checksum")
        self.sha256 = sha256

    def apply(self, stage: "spack.stage.Stage") -> None:
        """Apply a patch to source in a stage.

        Args:
            stage: stage where source code lives
        """
        assert self.stage.expanded, "Stage must be expanded before applying patches"

        # Get the patch file.
        files = os.listdir(self.stage.source_path)
        assert len(files) == 1, "Expected one file in stage source path, found %s" % files
        self.path = os.path.join(self.stage.source_path, files[0])

        return super().apply(stage)

    @property
    def stage(self) -> "spack.stage.Stage":
        """The stage in which to download (and unpack) the URL patch.

        Returns:
            The stage object.
        """
        if self._stage:
            return self._stage

        fetch_digest = self.archive_sha256 or self.sha256

        # Two checksums, one for compressed file, one for its contents
        if self.archive_sha256 and self.sha256:
            fetcher: spack.fetch_strategy.FetchStrategy = (
                spack.fetch_strategy.FetchAndVerifyExpandedFile(
                    self.url, archive_sha256=self.archive_sha256, expanded_sha256=self.sha256
                )
            )
        else:
            fetcher = spack.fetch_strategy.URLFetchStrategy(
                url=self.url, sha256=self.sha256, expand=False
            )

        # The same package can have multiple patches with the same name but
        # with different contents, therefore apply a subset of the hash.
        name = "{0}-{1}".format(os.path.basename(self.url), fetch_digest[:7])

        per_package_ref = os.path.join(self.owner.split(".")[-1], name)
        mirror_ref = spack.mirror.default_mirror_layout(fetcher, per_package_ref)
        self._stage = spack.stage.Stage(
            fetcher,
            name=f"{spack.stage.stage_prefix}patch-{fetch_digest}",
            mirror_paths=mirror_ref,
            mirrors=spack.mirror.MirrorCollection(source=True).values(),
        )
        return self._stage

    def to_dict(self) -> Dict[str, Any]:
        """Dictionary representation of the patch.

        Returns:
            A dictionary representation.
        """
        data = super().to_dict()
        data["url"] = self.url
        if self.archive_sha256:
            data["archive_sha256"] = self.archive_sha256
        return data


def from_dict(
    dictionary: Dict[str, Any], repository: Optional["spack.repo.RepoPath"] = None
) -> Patch:
    """Create a patch from json dictionary.

    Args:
        dictionary: dictionary representation of a patch
        repository: repository containing package

    Returns:
        A patch object.

    Raises:
        ValueError: If *owner* or *url*/*relative_path* are missing in the dictionary.
    """
    repository = repository or spack.repo.PATH
    owner = dictionary.get("owner")
    if owner is None:
        raise ValueError(f"Invalid patch dictionary: {dictionary}")
    assert isinstance(owner, str)
    pkg_cls = repository.get_pkg_class(owner)

    if "url" in dictionary:
        return UrlPatch(
            pkg_cls,
            dictionary["url"],
            dictionary["level"],
            working_dir=dictionary["working_dir"],
            # Added in v0.22, fallback required for backwards compatibility
            reverse=dictionary.get("reverse", False),
            sha256=dictionary["sha256"],
            archive_sha256=dictionary.get("archive_sha256"),
        )

    elif "relative_path" in dictionary:
        patch = FilePatch(
            pkg_cls,
            dictionary["relative_path"],
            dictionary["level"],
            dictionary["working_dir"],
            # Added in v0.22, fallback required for backwards compatibility
            dictionary.get("reverse", False),
        )

        # If the patch in the repo changes, we cannot get it back, so we
        # just check it and fail here.
        # TODO: handle this more gracefully.
        sha256 = dictionary["sha256"]
        checker = Checker(sha256)
        if patch.path and not checker.check(patch.path):
            raise spack.fetch_strategy.ChecksumError(
                "sha256 checksum failed for %s" % patch.path,
                "Expected %s but got %s " % (sha256, checker.sum)
                + "Patch may have changed since concretization.",
            )
        return patch
    else:
        raise ValueError("Invalid patch dictionary: %s" % dictionary)


class PatchCache:
    """Index of patches used in a repository, by sha256 hash.

    This allows us to look up patches without loading all packages.  It's
    also needed to properly implement dependency patching, as need a way
    to look up patches that come from packages not in the Spec sub-DAG.

    The patch index is structured like this in a file (this is YAML, but
    we write JSON)::

        patches:
            sha256:
                namespace1.package1:
                    <patch json>
                namespace2.package2:
                    <patch json>
                ... etc. ...
    """

    def __init__(
        self, repository: "spack.repo.RepoPath", data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize a new PatchCache instance.

        Args:
            repository: repository containing package
            data: nested dictionary of patches
        """
        if data is None:
            self.index = {}
        else:
            if "patches" not in data:
                raise IndexError("invalid patch index; try `spack clean -m`")
            self.index = data["patches"]

        self.repository = repository

    @classmethod
    def from_json(cls, stream: Any, repository: "spack.repo.RepoPath") -> "PatchCache":
        """Initialize a new PatchCache instance from JSON.

        Args:
            stream: stream of data
            repository: repository containing package

        Returns:
            A new PatchCache instance.
        """
        return PatchCache(repository=repository, data=sjson.load(stream))

    def to_json(self, stream: Any) -> None:
        """Dump a JSON representation to a stream.

        Args:
            stream: stream of data
        """
        sjson.dump({"patches": self.index}, stream)

    def patch_for_package(self, sha256: str, pkg: "spack.package_base.PackageBase") -> Patch:
        """Look up a patch in the index and build a patch object for it.

        We build patch objects lazily because building them requires that
        we have information about the package's location in its repo.

        Args:
            sha256: sha256 hash to look up
            pkg: Package object to get patch for.

        Returns:
            The patch object.
        """
        sha_index = self.index.get(sha256)
        if not sha_index:
            raise spack.error.PatchLookupError(
                f"Couldn't find patch for package {pkg.fullname} with sha256: {sha256}"
            )

        # Find patches for this class or any class it inherits from
        for fullname in pkg.fullnames:
            patch_dict = sha_index.get(fullname)
            if patch_dict:
                break
        else:
            raise spack.error.PatchLookupError(
                f"Couldn't find patch for package {pkg.fullname} with sha256: {sha256}"
            )

        # add the sha256 back (we take it out on write to save space,
        # because it's the index key)
        patch_dict = dict(patch_dict)
        patch_dict["sha256"] = sha256
        return from_dict(patch_dict, repository=self.repository)

    def update_package(self, pkg_fullname: str) -> None:
        """Update the patch cache.

        Args:
            pkg_fullname: package to update.
        """
        # remove this package from any patch entries that reference it.
        empty = []
        for sha256, package_to_patch in self.index.items():
            remove = []
            for fullname, patch_dict in package_to_patch.items():
                if patch_dict["owner"] == pkg_fullname:
                    remove.append(fullname)

            for fullname in remove:
                package_to_patch.pop(fullname)

            if not package_to_patch:
                empty.append(sha256)

        # remove any entries that are now empty
        for sha256 in empty:
            del self.index[sha256]

        # update the index with per-package patch indexes
        pkg_cls = self.repository.get_pkg_class(pkg_fullname)
        partial_index = self._index_patches(pkg_cls, self.repository)
        for sha256, package_to_patch in partial_index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    def update(self, other: "PatchCache") -> None:
        """Update this cache with the contents of another.

        Args:
            other: another patch cache to merge
        """
        for sha256, package_to_patch in other.index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    @staticmethod
    def _index_patches(
        pkg_class: Type["spack.package_base.PackageBase"], repository: "spack.repo.RepoPath"
    ) -> Dict[Any, Any]:
        """Patch index for a specific patch.

        Args:
            pkg_class: package object to get patches for
            repository: repository containing the package

        Returns:
            The patch index for that package.
        """
        index = {}

        # Add patches from the class
        for cond, patch_list in pkg_class.patches.items():
            for patch in patch_list:
                patch_dict = patch.to_dict()
                patch_dict.pop("sha256")  # save some space
                index[patch.sha256] = {pkg_class.fullname: patch_dict}

        for deps_by_name in pkg_class.dependencies.values():
            for dependency in deps_by_name.values():
                for patch_list in dependency.patches.values():
                    for patch in patch_list:
                        dspec_cls = repository.get_pkg_class(dependency.spec.name)
                        patch_dict = patch.to_dict()
                        patch_dict.pop("sha256")  # save some space
                        index[patch.sha256] = {dspec_cls.fullname: patch_dict}

        return index
