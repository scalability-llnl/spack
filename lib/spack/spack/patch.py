# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os
import os.path
import inspect

import llnl.util.filesystem
import llnl.util.lang

import spack.error
import spack.fetch_strategy as fs
import spack.repo
import spack.stage
import spack.util.spack_json as sjson
import spack

from spack.util.compression import allowed_archive
from spack.util.crypto import checksum, Checker
from spack.util.executable import which


def apply_patch(stage, patch_path, level=1, working_dir='.'):
    """Apply the patch at patch_path to code in the stage.

    Args:
        stage (spack.stage.Stage): stage with code that will be patched
        patch_path (str): filesystem location for the patch to apply
        level (int, optional): patch level (default 1)
        working_dir (str): relative path *within* the stage to change to
            (default '.')
    """
    patch = which("patch", required=True)
    with llnl.util.filesystem.working_dir(stage.source_path):
        patch('-s',
              '-p', str(level),
              '-i', patch_path,
              '-d', working_dir)


class Patch(object):
    """Base class for patches.

    Arguments:
        pkg (str): the package that owns the patch

    The owning package is not necessarily the package to apply the patch
    to -- in the case where a dependent package patches its dependency,
    it is the dependent's fullname.

    """
    def __init__(self, pkg, path_or_url, level, working_dir):
        # validate level (must be an integer >= 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

        # Attributes shared by all patch subclasses
        self.owner = pkg.fullname
        self.path_or_url = path_or_url  # needed for debug output
        self.path = None  # must be set before apply()
        self.level = level
        self.working_dir = working_dir

    def fetch(self):
        """Fetch the patch in case of a UrlPatch
        """

    def clean(self):
        """Clean up the patch stage in case of a UrlPatch"""

    def apply(self, stage):
        """Apply a patch to source in a stage.

        Arguments:
            stage (spack.stage.Stage): stage where source code lives
        """
        assert self.path, (
            "Path for patch not set in apply: %s" % self.path_or_url)

        if not os.path.isfile(self.path):
            raise NoSuchPatchError("No such patch: %s" % self.path)

        apply_patch(stage, self.path, self.level, self.working_dir)

    @property
    def stage(self):
        return None

    def to_dict(self):
        """Partial dictionary -- subclases should add to this."""
        return {
            'owner': self.owner,
            'sha256': self.sha256,
            'level': self.level,
            'working_dir': self.working_dir,
        }


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository.

    Arguments:
        pkg (str): the class object for the package that owns the patch
        relative_path (str): path to patch, relative to the repository
            directory for a package.
        level (int): level to pass to patch command
        working_dir (str): path within the source directory where patch
            should be applied
    """
    def __init__(self, pkg, relative_path, level, working_dir,
                 ordering_key=None):
        self.relative_path = relative_path

        # patches may be defined by relative paths to parent classes
        # search mro to look for the file
        abs_path = None
        # At different times we call FilePatch on instances and classes
        pkg_cls = pkg if inspect.isclass(pkg) else pkg.__class__
        for cls in inspect.getmro(pkg_cls):
            if not hasattr(cls, 'phases'):
                # We've gone too far up the MRO
                break

            # Cannot use pkg.package_dir because it's a property and we have
            # classes, not instances.
            pkg_dir = spack.repo.path.dirname_for_package_name(cls.name)
            path = os.path.join(pkg_dir, self.relative_path)
            if os.path.exists(path):
                abs_path = path
                break

        if abs_path is None:
            msg = 'FilePatch: Patch file %s for ' % relative_path
            msg += 'package %s.%s does not exist.' % (pkg.namespace, pkg.name)
            raise ValueError(msg)

        super(FilePatch, self).__init__(pkg, abs_path, level, working_dir)
        self.path = abs_path
        self._sha256 = None
        self.ordering_key = ordering_key

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = checksum(hashlib.sha256, self.path)
        return self._sha256

    def to_dict(self):
        return llnl.util.lang.union_dicts(
            super(FilePatch, self).to_dict(),
            {'relative_path': self.relative_path})


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL.

    Arguments:
        pkg (str): the package that owns the patch
        url (str): URL where the patch can be fetched
        level (int): level to pass to patch command
        working_dir (str): path within the source directory where patch
            should be applied
    """
    def __init__(self, pkg, url, level=1, working_dir='.', ordering_key=None,
                 **kwargs):
        super(UrlPatch, self).__init__(pkg, url, level, working_dir)

        self.url = url
        self._stage = None

        self.ordering_key = ordering_key

        self.archive_sha256 = kwargs.get('archive_sha256')
        if allowed_archive(self.url) and not self.archive_sha256:
            raise PatchDirectiveError(
                "Compressed patches require 'archive_sha256' "
                "and patch 'sha256' attributes: %s" % self.url)

        self.sha256 = kwargs.get('sha256')
        if not self.sha256:
            raise PatchDirectiveError("URL patches require a sha256 checksum")

    def fetch(self):
        """Retrieve the patch in a temporary stage and compute self.path

        Args:
            stage: stage for the package that needs to be patched
        """
        self.stage.create()
        self.stage.fetch()
        self.stage.check()

        root = self.stage.path
        if self.archive_sha256:
            self.stage.expand_archive()
            root = self.stage.source_path

        files = os.listdir(root)
        if not files:
            if self.archive_sha256:
                raise NoSuchPatchError(
                    "Archive was empty: %s" % self.url)
            else:
                raise NoSuchPatchError(
                    "Patch failed to download: %s" % self.url)

        self.path = os.path.join(root, files.pop())

        if not os.path.isfile(self.path):
            raise NoSuchPatchError(
                "Archive %s contains no patch file!" % self.url)

        # for a compressed archive, Need to check the patch sha256 again
        # and the patch is in a directory, not in the same place
        if self.archive_sha256 and spack.config.get('config:checksum'):
            checker = Checker(self.sha256)
            if not checker.check(self.path):
                raise fs.ChecksumError(
                    "sha256 checksum failed for %s" % self.path,
                    "Expected %s but got %s" % (self.sha256, checker.sum))

    @property
    def stage(self):
        if self._stage:
            return self._stage

        # use archive digest for compressed archives
        fetch_digest = self.sha256
        if self.archive_sha256:
            fetch_digest = self.archive_sha256

        fetcher = fs.URLFetchStrategy(self.url, fetch_digest,
                                      expand=bool(self.archive_sha256))

        # The same package can have multiple patches with the same name but
        # with different contents, therefore apply a subset of the hash.
        name = '{0}-{1}'.format(os.path.basename(self.url), fetch_digest[:7])

        per_package_ref = os.path.join(self.owner.split('.')[-1], name)
        # Reference starting with "spack." is required to avoid cyclic imports
        mirror_ref = spack.mirror.mirror_archive_paths(
            fetcher,
            per_package_ref)

        self._stage = spack.stage.Stage(fetcher, mirror_paths=mirror_ref)
        self._stage.create()
        return self._stage

    def clean(self):
        self.stage.destroy()

    def to_dict(self):
        data = super(UrlPatch, self).to_dict()
        data['url'] = self.url
        if self.archive_sha256:
            data['archive_sha256'] = self.archive_sha256
        return data


def from_dict(dictionary):
    """Create a patch from json dictionary."""
    owner = dictionary.get('owner')
    if 'owner' not in dictionary:
        raise ValueError('Invalid patch dictionary: %s' % dictionary)
    pkg = spack.repo.get(owner)

    if 'url' in dictionary:
        return UrlPatch(
            pkg,
            dictionary['url'],
            dictionary['level'],
            dictionary['working_dir'],
            sha256=dictionary['sha256'],
            archive_sha256=dictionary.get('archive_sha256'))

    elif 'relative_path' in dictionary:
        patch = FilePatch(
            pkg,
            dictionary['relative_path'],
            dictionary['level'],
            dictionary['working_dir'])

        # If the patch in the repo changes, we cannot get it back, so we
        # just check it and fail here.
        # TODO: handle this more gracefully.
        sha256 = dictionary['sha256']
        checker = Checker(sha256)
        if not checker.check(patch.path):
            raise fs.ChecksumError(
                "sha256 checksum failed for %s" % patch.path,
                "Expected %s but got %s" % (sha256, checker.sum),
                "Patch may have changed since concretization.")
        return patch
    else:
        raise ValueError("Invalid patch dictionary: %s" % dictionary)


class PatchCache(object):
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
    def __init__(self, data=None):
        if data is None:
            self.index = {}
        else:
            if 'patches' not in data:
                raise IndexError('invalid patch index; try `spack clean -m`')
            self.index = data['patches']

    @classmethod
    def from_json(cls, stream):
        return PatchCache(sjson.load(stream))

    def to_json(self, stream):
        sjson.dump({'patches': self.index}, stream)

    def patch_for_package(self, sha256, pkg):
        """Look up a patch in the index and build a patch object for it.

        Arguments:
            sha256 (str): sha256 hash to look up
            pkg (spack.package.Package): Package object to get patch for.

        We build patch objects lazily because building them requires that
        we have information about the package's location in its repo.

        """
        sha_index = self.index.get(sha256)
        if not sha_index:
            raise NoSuchPatchError(
                "Couldn't find patch for package %s with sha256: %s"
                % (pkg.fullname, sha256))

        patch_dict = sha_index.get(pkg.fullname)
        if not patch_dict:
            raise NoSuchPatchError(
                "Couldn't find patch for package %s with sha256: %s"
                % (pkg.fullname, sha256))

        # add the sha256 back (we take it out on write to save space,
        # because it's the index key)
        patch_dict = dict(patch_dict)
        patch_dict['sha256'] = sha256
        return from_dict(patch_dict)

    def update_package(self, pkg_fullname):
        # remove this package from any patch entries that reference it.
        empty = []
        for sha256, package_to_patch in self.index.items():
            remove = []
            for fullname, patch_dict in package_to_patch.items():
                if patch_dict['owner'] == pkg_fullname:
                    remove.append(fullname)

            for fullname in remove:
                package_to_patch.pop(fullname)

            if not package_to_patch:
                empty.append(sha256)

        # remove any entries that are now empty
        for sha256 in empty:
            del self.index[sha256]

        # update the index with per-package patch indexes
        pkg = spack.repo.get(pkg_fullname)
        partial_index = self._index_patches(pkg)
        for sha256, package_to_patch in partial_index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    def update(self, other):
        """Update this cache with the contents of another."""
        for sha256, package_to_patch in other.index.items():
            p2p = self.index.setdefault(sha256, {})
            p2p.update(package_to_patch)

    @staticmethod
    def _index_patches(pkg_class):
        index = {}

        # Add patches from the class
        for cond, patch_list in pkg_class.patches.items():
            for patch in patch_list:
                patch_dict = patch.to_dict()
                patch_dict.pop('sha256')  # save some space
                index[patch.sha256] = {pkg_class.fullname: patch_dict}

        # and patches on dependencies
        for name, conditions in pkg_class.dependencies.items():
            for cond, dependency in conditions.items():
                for pcond, patch_list in dependency.patches.items():
                    for patch in patch_list:
                        dspec = spack.repo.get(dependency.spec.name)
                        patch_dict = patch.to_dict()
                        patch_dict.pop('sha256')  # save some space
                        index[patch.sha256] = {dspec.fullname: patch_dict}

        return index


class NoSuchPatchError(spack.error.SpackError):
    """Raised when a patch file doesn't exist."""


class PatchDirectiveError(spack.error.SpackError):
    """Raised when the wrong arguments are suppled to the patch directive."""
