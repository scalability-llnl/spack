# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VotcaCtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the VOTCA charge transport engine.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/ctp/tarball/v1.5"
    git = "https://github.com/votca/ctp.git"

    version(
        "1.5.1",
        sha256="ef957c2f6b09335d0d27ecb7e1b80b55e76a100247bc0d0b3cfef7718d2a1126",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="31eb6bcc9339e575116f0c91fe7a4ce7d4189f31f0640329c993fea911401d65",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
    depends_on("votca-tools@1.5.1")
    depends_on("votca-csg@1.5.1")
    depends_on("gsl")
