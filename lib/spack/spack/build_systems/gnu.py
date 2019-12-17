# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

import spack.package


class GNUMirrorPackage(spack.package.PackageBase):
    """Mixin that takes care of setting url and mirrors for GNU packages."""
    #: Path of the package in a GNU mirror
    gnu_mirror_path = None

    #: List of GNU mirrors used by Spack
    base_mirrors = [
        'https://ftp.gnu.org/gnu',
        'https://ftpmirror.gnu.org/',
        # Fall back to http if https didn't work (for instance because
        # Spack is bootstrapping curl)
        'http://ftpmirror.gnu.org/'
    ]

    @property
    def urls(self):
        self._ensure_gnu_mirror_path_is_set_or_raise()
        return [
            os.path.join(m, self.gnu_mirror_path) for m in self.base_mirrors
        ]

    def _ensure_gnu_mirror_path_is_set_or_raise(self):
        if self.gnu_mirror_path is None:
            cls_name = type(self).__name__
            msg = ('{0} must define a `gnu_mirror_path` attribute'
                   ' [none defined]')
            raise AttributeError(msg.format(cls_name))
