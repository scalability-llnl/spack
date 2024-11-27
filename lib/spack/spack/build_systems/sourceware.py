# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Optional

import spack.package_base
import spack.util.url


class SourcewarePackage(spack.package_base.PackageBase):
    """Mixin that takes care of setting url and mirrors for Sourceware.org
    packages."""

    #: Path of the package in a Sourceware mirror
    sourceware_mirror_path: Optional[str] = None

    #: List of Sourceware mirrors used by Spack
    base_mirrors = [
        "https://sourceware.org/pub/",
        "https://mirrors.kernel.org/sourceware/",
        "https://ftp.gwdg.de/pub/linux/sources.redhat.com/",
    ]

    @property
    def urls(self):
        self._ensure_sourceware_mirror_path_is_set_or_raise()
        return [
            spack.util.url.join(m, self.sourceware_mirror_path, resolve_href=True)
            for m in self.base_mirrors
        ]

    def _ensure_sourceware_mirror_path_is_set_or_raise(self):
        if self.sourceware_mirror_path is None:
            cls_name = type(self).__name__
            msg = "{0} must define a `sourceware_mirror_path` attribute" " [none defined]"
            raise AttributeError(msg.format(cls_name))
