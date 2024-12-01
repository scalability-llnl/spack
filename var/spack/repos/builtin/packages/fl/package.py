# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    "0.79.47": {
        "Linux-x86_64": (
            "b8a4a74118c1a024313bf912261fbc016a53f2d15adb1226217f2a10a9f7ca9a",
            "https://www.flxpert.hu/fl/fl_0.79.47-amd64-linux.tar.gz",
        ),
        "Linux-aarch64": (
            "3ff052013daf319927d04ba83b8f90c12575983911faf6c1559437062032b669",
            "http://www.flxpert.hu/fl/fl_0.79.47-aarch64-linux.tar.gz",
        ),
    }
}


class Fl(Package):
    """Fawlty Language is an IDL8
    (Interactive Data Language) compatible compiler."""

    homepage = "https://www.flxpert.hu/fl/"
    url = "https://www.flxpert.hu/fl/fl_0.79.47-amd64-linux.tar.gz"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    def install(self, spec, prefix):
        if self.spec.satisfies("platform=linux") and self.spec.target.family in [
            "x86_64",
            "aarch64",
        ]:
            with working_dir("fl_{0}".format(spec.version)):
                install_tree(".", prefix)
        else:
            raise InstallError("fl requires Linux x86_64 or aarch64 platform.")
