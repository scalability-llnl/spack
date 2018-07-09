##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import os.path
import inspect
import hashlib

import spack.error
import spack.fetch_strategy as fs
import spack.stage
from spack.util.crypto import checksum, Checker
from llnl.util.filesystem import working_dir
from spack.util.executable import which
from spack.util.compression import allowed_archive


def absolute_path_for_package(pkg):
    """Returns the absolute path to the ``package.py`` file implementing
    the recipe for the package passed as argument.

    Args:
        pkg: a valid package object, or a Dependency object.
    """
    if isinstance(pkg, spack.dependency.Dependency):
        pkg = pkg.pkg
    m = inspect.getmodule(pkg)
    return os.path.abspath(m.__file__)


class Patch(object):
    """Base class to describe a patch that needs to be applied to some
    expanded source code.
    """

    @staticmethod
    def create(pkg, path_or_url, level=1, working_dir=".", **kwargs):
        """
        Factory method that creates an instance of some class derived from
        Patch

        Args:
            pkg: package that needs to be patched
            path_or_url: path or url where the patch is found
            level: patch level (default 1)
            working_dir (str): dir to change to before applying (default '.')

        Returns:
            instance of some Patch class
        """
        # Check if we are dealing with a URL
        if '://' in path_or_url:
            return UrlPatch(path_or_url, level, working_dir, **kwargs)
        # Assume patches are stored in the repository
        return FilePatch(pkg, path_or_url, level, working_dir)

    def __init__(self, path_or_url, level, working_dir):
        # Check on level (must be an integer > 0)
        if not isinstance(level, int) or not level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")
        # Attributes shared by all patch subclasses
        self.path_or_url = path_or_url
        self.level = level
        self.working_dir = working_dir
        # self.path needs to be computed by derived classes
        # before a call to apply
        self.path = None

        if not isinstance(self.level, int) or not self.level >= 0:
            raise ValueError("Patch level needs to be a non-negative integer.")

    def apply(self, stage):
        """Apply the patch at self.path to the source code in the
        supplied stage

        Args:
            stage: stage for the package that needs to be patched
        """
        patch = which("patch", required=True)
        with working_dir(stage.source_path):
            # Use -N to allow the same patches to be applied multiple times.
            patch('-s', '-p', str(self.level), '-i', self.path,
                  "-d", self.working_dir)


class FilePatch(Patch):
    """Describes a patch that is retrieved from a file in the repository"""
    def __init__(self, pkg, path_or_url, level, working_dir):
        super(FilePatch, self).__init__(path_or_url, level, working_dir)

        pkg_dir = os.path.dirname(absolute_path_for_package(pkg))
        self.path = os.path.join(pkg_dir, path_or_url)
        if not os.path.isfile(self.path):
            raise NoSuchPatchError(
                "No such patch for package %s: %s" % (pkg.name, self.path))
        self._sha256 = None

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = checksum(hashlib.sha256, self.path)
        return self._sha256


class UrlPatch(Patch):
    """Describes a patch that is retrieved from a URL"""
    def __init__(self, path_or_url, level, working_dir, **kwargs):
        super(UrlPatch, self).__init__(path_or_url, level, working_dir)
        self.url = path_or_url

        self.archive_sha256 = None
        if allowed_archive(self.url):
            if 'archive_sha256' not in kwargs:
                raise PatchDirectiveError(
                    "Compressed patches require 'archive_sha256' "
                    "and patch 'sha256' attributes: %s" % self.url)
            self.archive_sha256 = kwargs.get('archive_sha256')

        if 'sha256' not in kwargs:
            raise PatchDirectiveError("URL patches require a sha256 checksum")
        self.sha256 = kwargs.get('sha256')

    def apply(self, stage):
        """Retrieve the patch in a temporary stage, computes
        self.path and calls `super().apply(stage)`

        Args:
            stage: stage for the package that needs to be patched
        """
        is_archive = spack.util.compression.allowed_archive(self.url)
        # use archive digest for compressed archives
        fetch_digest = self.sha256
        if self.archive_sha256:
            fetch_digest = self.archive_sha256

        fetcher = fs.URLFetchStrategy(self.url, digest=fetch_digest,
                                      expand=is_archive)
        mirror = os.path.join(
            os.path.dirname(stage.mirror_path),
            os.path.basename(self.url))

        with spack.stage.Stage(fetcher, mirror_path=mirror) as patch_stage:
            patch_stage.fetch()
            patch_stage.check()
            patch_stage.cache_local()
            patch_stage.setup_source()
            root = patch_stage.source_path

            files = os.listdir(root)
            if not files:
                if self.archive_sha256:
                    raise NoSuchPatchError(
                        "Archive was empty: %s" % self.url)
                else:
                    raise NoSuchPatchError(
                        "Patch failed to download: %s" % self.url)

            # archive patches are assumed to consist of one file, so regardless
            # of whether the patch is compressed there should always be only
            # one file in the staging directory
            self.path = os.path.join(root, files.pop())

            if not os.path.isfile(self.path):
                raise NoSuchPatchError(
                    "Archive %s contains no patch file!" % self.url)

            # for a compressed archive, Need to check the patch sha256 again
            # and the patch is in a directory, not in the same place
            if self.archive_sha256:
                checker = Checker(self.sha256)
                if not checker.check(self.path):
                    raise fs.ChecksumError(
                        "sha256 checksum failed for %s" % self.path,
                        "Expected %s but got %s" % (self.sha256, checker.sum))

            super(UrlPatch, self).apply(stage)


class NoSuchPatchError(spack.error.SpackError):
    """Raised when a patch file doesn't exist."""


class PatchDirectiveError(spack.error.SpackError):
    """Raised when the wrong arguments are suppled to the patch directive."""
