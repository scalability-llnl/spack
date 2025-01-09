# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Makedepf90(AutotoolsPackage):
    """Makedepf90 is a program for automatic creation of Makefile-style dependency lists for
    Fortran source code."""

    homepage = "https://salsa.debian.org/science-team/makedepf90"
    url = "https://deb.debian.org/debian/pool/main/m/makedepf90/makedepf90_3.0.1.orig.tar.xz"

    maintainers("tukss")

    license("GPL-2.0-only", checked_by="tukss")

    version("3.0.1", sha256="a11601ea14ad793f23fca9c7e7df694b6337f962ccc930d995d72e172edf29ee")

    depends_on("c", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
