# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Chaplin(AutotoolsPackage):
    """The FORTRAN library CHAPLIN enables you to numerically
    evaluate Harmonic polylogarithms up to weight 4 for any
    complex argument."""

    homepage = "https://chaplin.hepforge.org"
    url = "https://chaplin.hepforge.org/code/chaplin-1.2.tar"

    tags = ["hep"]

    maintainers("vvolkl")

    version("1.2", sha256="f17c2d985fd4e4ce36cede945450416d3fa940af68945c91fa5d3ca1d76d4b49")

    depends_on("fortran", type="build")  # generated
