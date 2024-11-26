# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cans(MakefilePackage):
    """CaNS (Canonical Navier-Stokes) is a code for
    massively-parallel numerical simulations of fluid
    flows. It aims at solving any fluid flow of an
    incompressible, Newtonian fluid that can benefit
    from a FFT-based solver for the second-order
    finite-difference Poisson equation
    in a 3D Cartesian grid."""

    homepage = "https://github.com/CaNS-World/CaNS"
    url = "https://github.com/CaNS-World/CaNS/archive/refs/tags/v1.1.4.tar.gz"

    maintainers("lhxone", "p-costa", "nscapin", "GabrieleBoga")

    license("MIT")

    version("1.1.4", sha256="8334c67810472edc18d5403a0bcb27fd57a620722c1e8c317518db4506867b81")
    version("1.1.3", sha256="01fa42e51ddcf6161fb63a124a0f2218c67f85ff4cc5236b995a5650d85e7615")
    version("1.1.2", sha256="31c8d6c1f619fb60b7919922c7a3a64dd614a1a2f89f38560184f75ed0526171")
    version("1.1.0", sha256="e3fd84902e18715c6476fe780e2395ca04db9e6b0c830b55a7aa9204b1fd0886")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("fftw")

    def edit(self, spec, prefix):
        with working_dir("src"):
            makefile = FileFilter("Makefile")
            makefile.filter(
                "LIBS =.*", "LIBS = -L{} -lfftw3 -lfftw3_threads".format(spec["fftw"].prefix.lib)
            )

    def build(self, spec, prefix):
        with working_dir("src"):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir("src"):
            install("cans", prefix.bin)
