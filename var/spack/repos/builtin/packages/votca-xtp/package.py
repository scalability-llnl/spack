# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VotcaXtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the VOTCA exciton transport engine.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/xtp/tarball/v1.4.1"
    git = "https://github.com/votca/xtp.git"
    maintainers("junghans")

    version("stable", branch="stable", deprecated=True)
    version(
        "2021.2",
        sha256="a13180cc05a24c441326a2b209e4d1cc6b176f1b8d7aec1aea46b627e230ff8c",
        deprecated=True,
    )
    version(
        "2021.1",
        sha256="8ce112fc40676690369133188848dfeb3875d57351286cad4c312057a4dd767b",
        deprecated=True,
    )
    version(
        "2021",
        sha256="43bb5a52fec675738f4b5896f0833a1c1090bd7e74f97769697495abf4652e40",
        deprecated=True,
    )
    version(
        "1.6.4",
        sha256="699a835954556cf6b2f20dac7942c1761c6dd6c6c3fbdde62c8bfcfd71ee075b",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="757b9a6a470b3c356f638d62269c5b72b8ace374f006658aef8bb6afd1ad1413",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="b51a28cddceca6998b981ad61466617ad624d577ce424c0653d92a680f460061",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="886af50bc12457bbafb06dc927b7fd4cadc3db1b4615b24a08953f6b358debef",
        deprecated=True,
    )
    version(
        "1.6",
        sha256="695c2d9d3f924103481529f992e3723bdce10b8edfc294421a849cdf51dbbb6e",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="17a7722e5a32d236e4f1f6f88b680da4ba5f52bcf65bca3687c6a1c731d10881",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="b40b6d19e13f0650e84b8beebe86ce5c09071624f18d66df826f9d8584b4d3c8",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="4b53d371d6cf648c9e9e9bd1f104d349cafeaf10a02866e3f1d05c574b595a21",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
    for v in [
        "1.4.1",
        "1.5",
        "1.5.1",
        "1.6",
        "1.6.1",
        "1.6.2",
        "1.6.3",
        "1.6.4",
        "2021",
        "2021.1",
        "2021.2",
        "stable",
    ]:
        depends_on("votca-tools@%s" % v, when="@%s:%s.0" % (v, v))
        depends_on("votca-csg@%s" % v, when="@%s:%s.0" % (v, v))
    depends_on("libxc", when="@stable,1.5:")
    depends_on("ceres-solver", when="@1.5:1.5.9999")
    depends_on("hdf5+cxx~mpi")
    depends_on("libint@2.6.0:", when="@2021:")
