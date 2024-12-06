# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
#  - the newest non-cuda version should be set as 'preferred_ver'
#  - a cuda dependency must be set for each new cuda version

_versions = {
    "6.1.7-cuda": {
        "Linux-x86_64": (
            "c3dd8f8b7567061a155d1921586dd95540410b35b2ccb8a33a463d9db8642711",
            "https://cdn.oxfordnanoportal.com/software/analysis/ont-guppy_6.1.7_linux64.tar.gz",
        ),
        "Linux-aarch64": (
            "e821fe85b538e1a5d38c17c8fc7497f6fad200ff9fdf0c98921b4d7b1d490914",
            "https://cdn.oxfordnanoportal.com/software/analysis/ont-guppy_6.1.7_linuxaarch64_cuda10.tar.gz",
        ),
    },
    "6.1.7": {
        "Linux-x86_64": (
            "4540441ca5393d76f05485f38cdba2dc0b5785af31d77006bdc3664b3f2644cb",
            "https://cdn.oxfordnanoportal.com/software/analysis/ont-guppy-cpu_6.1.7_linux64.tar.gz",
        )
    },
}


class OntGuppy(Package):
    """Guppy: local accelerated basecalling for Nanopore data"""

    homepage = "https://community.nanoporetech.com/downloads/guppy/release_notes"
    preferred_ver = "6.1.7"

    preferred_defined = False
    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            is_preferred = not preferred_defined and (ver == preferred_ver)
            if is_preferred:
                preferred_defined = True

            version(ver, sha256=pkg[0], url=pkg[1], preferred=is_preferred)

    depends_on("cuda@11.0.0:", when="@6.1.7-cuda", type="run")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("data", prefix.data)
        install_tree("lib", prefix.lib)
