# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VotcaCsgapps(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the VOTCA coarse-graining extra apps.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/csgapps/tarball/v1.4"
    git = "https://github.com/votca/csgapps.git"
    maintainers("junghans")

    version(
        "1.6.4",
        sha256="ef3d6fbc7f2ff2f29af7d170a5351ae3c37f52ca4c2b1697b1d2e30c26ff4eb1",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="fdb6a94eabdfe1bfae6002da16e364086d036c2dc24700a941b73d5bb1afc422",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="f7db0bda27d4419c570f44dc60d04b1fd7b4cdcf10db6301005fca70111fcfe3",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="03c7cef2a76e73cf953b2b5ea2cdca765ec1a2627d0a9d8869d46166e63d197c",
        deprecated=True,
    )
    version(
        "1.6",
        sha256="084bbc5b179bb7eb8f6671d2d5fa13e69e68946570c9120a7e4b10aff1866e2e",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="b4946711e88a1745688b6cce5aad872e6e2ea200fededf38d77a864883e3750e",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="18b40ce6222509bc70aa9d56b8c538cd5903edf7294d6f95530668e555206d5b",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="095d9ee4cd49d2fd79c10e0e84e6890b755e54dec6a5cd580a2b4241ba230a2b",
        deprecated=True,
    )
    version(
        "1.4",
        sha256="4ea8348c2f7de3cc488f48fbd8652e69b52515441952766c06ff67ed1aaf69a0",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    for v in ["1.4", "1.4.1", "1.5", "1.5.1", "1.6", "1.6.1", "1.6.2", "1.6.3", "1.6.4"]:
        depends_on("votca-csg@%s" % v, when="@%s:%s.0" % (v, v))
    depends_on("boost+exception+math+serialization+container")
