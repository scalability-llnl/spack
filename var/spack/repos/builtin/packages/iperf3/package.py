# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iperf3(AutotoolsPackage):
    """The iperf series of tools perform active measurements to determine the
    maximum achievable bandwidth on IP networks. iperf2 is a separately
    maintained project."""

    homepage = "https://software.es.net/iperf/"
    url = "https://downloads.es.net/pub/iperf/iperf-3.17.tar.gz"

    license("BSD-3-Clause-LBNL")

    version("3.17.1", sha256="84404ca8431b595e86c473d8f23d8bb102810001f15feaf610effd3b318788aa")
    version("3.17", sha256="077ede831b11b733ecf8b273abd97f9630fd7448d3ec1eaa789f396d82c8c943")
    version("3.16", sha256="cc740c6bbea104398cc3e466befc515a25896ec85e44a662d5f4a767b9cf713e")
    version("3.14", sha256="723fcc430a027bc6952628fa2a3ac77584a1d0bd328275e573fc9b206c155004")
    version("3.12", sha256="72034ecfb6a7d6d67e384e19fb6efff3236ca4f7ed4c518d7db649c447e1ffd6")
    version("3.9", sha256="24b63a26382325f759f11d421779a937b63ca1bc17c44587d2fcfedab60ac038")
    version("3.6", sha256="de5d51e46dc460cc590fb4d44f95e7cad54b74fea1eba7d6ebd6f8887d75946e")

    depends_on("c", type="build")  # generated
