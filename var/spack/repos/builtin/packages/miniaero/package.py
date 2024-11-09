# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Miniaero(MakefilePackage):
    """Proxy Application. MiniAero is a mini-application for the evaulation
    of programming models and hardware for next generation platforms.
    """

    homepage = "https://mantevo.org"
    git = "https://github.com/Mantevo/miniAero.git"

    tags = ["proxy-app"]

    version("2016-11-11", commit="f46d135479a5be19ec5d146ccaf0e581aeff4596")

    depends_on("cxx", type="build")  # generated

    depends_on("kokkos-legacy")

    @property
    def build_targets(self):
        targets = [
            "--directory=kokkos",
            "CXX=c++",
            "KOKKOS_PATH={0}".format(self.spec["kokkos-legacy"].prefix),
        ]

        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("kokkos/miniAero.host", prefix.bin)
        install("kokkos/README", prefix.doc)
        install("kokkos/tests/3D_Sod_Serial/miniaero.inp", prefix.bin)
        install_tree("kokkos/tests", prefix.doc.tests)
