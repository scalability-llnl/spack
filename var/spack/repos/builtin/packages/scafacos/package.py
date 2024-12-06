# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scafacos(AutotoolsPackage):
    """ScaFaCoS is a library of scalable fast coulomb solvers."""

    homepage = "http://www.scafacos.de/"
    url = "https://github.com/scafacos/scafacos/releases/download/v1.0.4/scafacos-1.0.4.tar.gz"

    maintainers("hmenke")

    license("GPL-3.0-or-later OR LGPL-3.0-or-later")

    version("1.0.4", sha256="6634c4202e825e771d1dd75bbe9cac5cee41136c87653fde98fbd634681c1be6")
    version("1.0.3", sha256="d3579f4cddb10a562722c190c2452ebc455592d44f6dbde8f155849ba6e2b3d0")
    version("1.0.2", sha256="158078665e48e28fd12b7895063db056cee5d135423fc36802e39c9160102b97")
    version("1.0.1", sha256="2b125f313795c81b0e87eb920082e91addf94c17444f9486d979e691aaded99b")
    version("1.0.0", sha256="cc5762edbecfec0323126b6a6a535dcc3e134fcfef4b00f63eb05fae15244a96")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("fftw")
    depends_on("file")
    depends_on("gmp")
    depends_on("gsl")
    depends_on("mpi")
    depends_on("pfft")
    depends_on("pnfft")

    def configure_args(self):
        args = [
            "--disable-doc",
            "--enable-fcs-solvers=direct,ewald,fmm,p3m",
            "FC={0}".format(self.spec["mpi"].mpifc),
            "F77={0}".format(self.spec["mpi"].mpif77),
        ]
        return args
