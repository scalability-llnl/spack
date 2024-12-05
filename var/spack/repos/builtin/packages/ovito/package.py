# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ovito(Package):
    """OVITO is a scientific visualization and analysis software for atomistic
    and particle simulation data. It helps scientists gain better insights into
    materials phenomena and physical processes. OVITO Basic is freely available
    for all major platforms under an open source license. It has served in a
    growing number of computational simulation studies as a powerful tool to
    analyze, understand and illustrate simulation results."""

    homepage = "https://www.ovito.org"
    url = "https://www.ovito.org/download/master/ovito-basic-3.6.0-x86_64.tar.xz"

    license("MIT")

    version("3.6.0", sha256="6ac43a3a39b1ec3cccab577602756a8b7010cc1f1f046c4f6a939590d12f0339")

    def install(self, spec, prefix):
        # Once we've unpacked the tarball, copy it's contents to the prefix
        copy_tree(".", prefix)
