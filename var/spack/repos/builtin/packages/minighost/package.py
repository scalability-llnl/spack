# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import tarfile

from spack.package import *


class Minighost(MakefilePackage):
    """Proxy Application. A Finite Difference proxy
    application which implements a difference stencil
    across a homogenous three dimensional domain.
    """

    homepage = "https://mantevo.org"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/MiniGhost/miniGhost_1.0.1.tar.gz"

    tags = ["proxy-app"]

    license("LGPL-3.0-only")

    version("1.0.1", sha256="713f305559d892923cde0ad3cbc53c7cefc52a684f65275ccc9fb0b1d049cccc")

    variant("mpi", default=True, description="Enable MPI Support")

    depends_on("mpi", when="+mpi")

    parallel = False

    @property
    def build_targets(self):
        targets = ["--directory=miniGhost_ref"]

        if "+mpi" in self.spec:
            targets.append("PROTOCOL=-D_MG_MPI")
            targets.append("FC={0}".format(self.spec["mpi"].mpif77))
            # CC is only used for linking, use it to pull in the right f77 libs
            targets.append("CC={0}".format(self.spec["mpi"].mpif77))
        else:
            targets.append("PROTOCOL=-D_MG_SERIAL")
            targets.append("FC=f77")
            targets.append("CC=cc")

        if "%gcc" in self.spec:
            targets.append("COMPILER_SUITE=gnu")
            targets.append("LIBS=-lm -lgfortran")
        elif "%cce" in self.spec:
            targets.append("COMPILER_SUITE=cray")
        elif "%intel" in self.spec:
            targets.append("COMPILER_SUITE=intel")

        return targets

    def edit(self, spec, prefix):
        inner_tar = tarfile.open("miniGhost_ref_{0}.tar.gz".format(self.version.up_to(3)))
        inner_tar.extractall()

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("miniGhost_ref/miniGhost.x", prefix.bin)
        install("miniGhost_ref/default-settings.h", prefix.bin)

        if "+mpi" in spec:
            install("miniGhost_ref/runtest.mpi", prefix.bin)
            install("miniGhost_ref/runtest.mpi.ds", prefix.bin)
        else:
            install("miniGhost_ref/runtest.serial", prefix.bin)

        install("README", prefix.doc)
