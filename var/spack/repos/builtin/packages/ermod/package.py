# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ermod(AutotoolsPackage):
    """ERmod (Energy Representation Module) is a program to calculate the
    solvation free energy based on the energy representation method. The
    program allows users to calculate the solvation free energy to arbitrary
    solvents, including inhomogeneous systems, and can run in cooperation with
    state-of-art molecular simulation softwares, such as NAMD, GROMACS and/or
    AMBER."""

    homepage = "https://sourceforge.net/projects/ermod/"
    url = (
        "https://sourceforge.net/projects/ermod/files/ermod-0.3%20%28stable%29/ermod-0.3.5.tar.gz"
    )

    license("GPL-2.0-or-later")

    version("0.3.6", sha256="8fdd8e0844fcc34cda2bbbf8ad03168c1c2f1409e06967a96a0f2269bb5f1b6b")
    version("0.3.5", sha256="42043ba7f53e9b74d0327b9982f33a4b79ed6964fbeb409e33178a6dcdf9e827")

    depends_on("fftw")
    depends_on("blas")

    def configure_args(self):
        args = ["--with-blas=%s" % self.spec["blas"].libs.ld_flags]
        return args
