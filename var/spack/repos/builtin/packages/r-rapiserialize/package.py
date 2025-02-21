# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRapiserialize(RPackage):
    """R API Serialization.

    This package provides other packages with access to the internal R
    serialization code. Access to this code is provided at the C function level
    by using the registration of native function mechanism. Client packages
    simply include a single header file RApiSerializeAPI.h provided by this
    package. This packages builds on the Rhpc package by Junji Nakano and Ei-ji
    Nakama which also includes a (partial) copy of the file
    src/main/serialize.c from R itself. The R Core group is the original author
    of the serialization code made available by this package."""

    cran = "RApiSerialize"

    maintainers("dorton21")

    version("0.1.3", sha256="9f413759eabb2acce2b9a363687ca365e1bbedaf9851d23a2ec3683a3d46f42b")
    version("0.1.2", sha256="9cc0bbb918eeadb394339c64b15324e8123fbb0061692f40102b111417a2600a")
    version("0.1.0", sha256="324d42c655c27b4647d194bfcd7c675da95c67ea3a74ce99853502022792a23e")
