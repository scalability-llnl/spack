# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cbc(AutotoolsPackage):
    """Cbc (Coin-or branch and cut) is an open-source mixed integer
    linear programming solver written in C++. It can be used as a
    callable library or using a stand-alone executable."""

    homepage = "https://projects.coin-or.org/Cbc"
    url = "https://github.com/coin-or/Cbc/archive/releases/2.10.5.tar.gz"

    license("EPL-2.0")

    version("2.10.11", sha256="1fb591dd88336fdaf096b8e42e46111e41671a5eb85d4ee36e45baff1678bd33")
    version("2.10.9", sha256="96d02593b01fd1460d421f002734384e4eb1e93ebe1fb3570dc2b7600f20a27e")
    version("2.10.8", sha256="8525abb541ee1b8e6ff03b00411b66e98bbc58f95be1aefd49d2bca571be2eaf")
    version("2.10.5", sha256="cc44c1950ff4615e7791d7e03ea34318ca001d3cac6dc3f7f5ee392459ce6719")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("coinutils")
    depends_on("osi")
    depends_on("cgl")

    build_directory = "spack-build"
