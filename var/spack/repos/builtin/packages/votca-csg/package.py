# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VotcaCsg(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the VOTCA coarse-graining engine.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/csg/tarball/v1.4"
    git = "https://github.com/votca/csg.git"
    maintainers("junghans")

    version("stable", branch="stable", deprecated=True)
    version(
        "2021.2",
        sha256="4c58ea90cc1b7fe95f7bc00634faadba945316417e741192d715cea6aa83f4ac",
        deprecated=True,
    )
    version(
        "2021.1",
        sha256="1e9cf90ddd7539e711e795292b721a4ee130a2089e659fa068a12960b77fff14",
        deprecated=True,
    )
    version(
        "2021",
        sha256="d66c9b30ce2a56d630d5db281444447d398be643005ebea70d3735fb60357305",
        deprecated=True,
    )
    version(
        "1.6.4",
        sha256="eae771b623f3c3edb09744030d053f10c75d64bad919df26c4f9bf3bfaa1cf86",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="35456b1f3116364b10ada37d99798294bd2d3df2e670cef3936251f88036ef88",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="96b244b282005259832ed6ec0dc22dafe132dcfc3d73dcd8e53b62f40befb545",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="ed12bcb1ccdf71f54e21cdcc9803add4b8ebdc6b8263cb5b0034f5db01e31dbb",
        deprecated=True,
    )
    version(
        "1.6",
        sha256="8cf6a4ac3ef7347c720a44d8a676f8cbd1462e162f6113de39f27b89354465ea",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="7fca1261bd267bf38d2edd26259730fed3126c0c3fd91fb81940dbe17bb568fd",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="160387cdc51f87dd20ff2e2eed97086beee415d48f3c92f4199f6109068c8ff4",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="41dccaecadd0165c011bec36a113629e27745a5a133d1a042efe4356acdb5450",
        deprecated=True,
    )
    version(
        "1.4",
        sha256="c13e7febd792de8c3d426203f089bd4d33b8067f9db5e8840e4579c88b61146e",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
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
        depends_on("votca-tools@%s" % v, when="@%s:%s.0" % (v, v))
    depends_on("boost+exception+filesystem+system+serialization+container+math+regex")
    depends_on("gromacs~mpi@5.1:2019")
    depends_on("hdf5~mpi")
