# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class VotcaCsgTutorials(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the VOTCA coarse-graining tutorials.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/csg-tutorials/tarball/v1.4"
    git = "https://github.com/votca/csg-tutorials.git"
    maintainers("junghans")

    version("stable", branch="stable", deprecated=True)
    version(
        "2021.2",
        sha256="156c5ec55a288e3013d393e66a1d2f09ebf4f14056d50d081535004696e7f5ba",
        deprecated=True,
    )
    version(
        "2021.1",
        sha256="5ea1e6ca370e6e7845f9195495f5fb8bbd72d601980e123ae7852f491f03949a",
        deprecated=True,
    )
    version(
        "2021",
        sha256="2b85c69007bb7d773529020e55fd82fed65651ee21eedccca9a801ab248ece97",
        deprecated=True,
    )
    version(
        "1.6.4",
        sha256="34ef40db6b178a7f513f8a6f43e7caff6ecb498d66d7bf8bc44900bc7aea31dc",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="709582b978d84f9de09ae6c3ba4ed28daec886d4e0431bc7d19c7246bd65f0b1",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="7c25e76391f3ffdd15f8a91aeed2d3ce7377591f128ed4ae34b36eca20e5af8f",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="d8428c4a03ce42d88317045ec555af3defa022fd9a61f05e07b57c5577288c8c",
        deprecated=True,
    )
    version(
        "1.6",
        sha256="54946c647724f1beb95942d47ec7f4cf7a95a59ec7268522693d5ec723585daf",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="e35cea92df0e7d05ca7b449c1b5d84d887a3a23c7796abe3b84e4d6feec7faca",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="03b841fb94129cf59781a7a5e3b71936c414aa9dfa17a50d7bc856d46274580c",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="623724192c3a7d76b603a74a3326f181045f10f38b9f56dce754a90f1a74556e",
        deprecated=True,
    )
    version(
        "1.4",
        sha256="27d50acd68a9d8557fef18ec2b0c62841ae91c22275ab9afbd65c35e4dd5f719",
        deprecated=True,
    )

    for v in [
        "1.4",
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
        depends_on("votca-csg@%s" % v, when="@%s:%s.0" % (v, v))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
