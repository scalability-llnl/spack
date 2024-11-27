# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional

import spack.package_base
import spack.util.url


class SourceforgePackage(spack.package_base.PackageBase):
    """Mixin that takes care of setting url and mirrors for Sourceforge
    packages."""

    #: Path of the package in a Sourceforge mirror
    sourceforge_mirror_path: Optional[str] = None

    #: List of Sourceforge mirrors used by Spack
    base_mirrors = [
        "https://prdownloads.sourceforge.net/",
        "https://freefr.dl.sourceforge.net/",
        "https://netcologne.dl.sourceforge.net/",
        "https://pilotfiber.dl.sourceforge.net/",
        "https://downloads.sourceforge.net/",
        "http://kent.dl.sourceforge.net/sourceforge/",
    ]

    @property
    def urls(self):
        self._ensure_sourceforge_mirror_path_is_set_or_raise()
        return [
            spack.util.url.join(m, self.sourceforge_mirror_path, resolve_href=True)
            for m in self.base_mirrors
        ]

    def _ensure_sourceforge_mirror_path_is_set_or_raise(self):
        if self.sourceforge_mirror_path is None:
            cls_name = type(self).__name__
            msg = "{0} must define a `sourceforge_mirror_path` attribute" " [none defined]"
            raise AttributeError(msg.format(cls_name))
