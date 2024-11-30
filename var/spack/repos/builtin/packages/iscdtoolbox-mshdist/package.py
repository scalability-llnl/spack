# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IscdtoolboxMshdist(CMakePackage):
    """Mshdist is a simple algorithm to generate the signed distance function
    to given objects in two and three space dimensions."""

    homepage = "https://github.com/ISCDtoolbox"
    url = "https://github.com/ISCDtoolbox/Mshdist/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/ISCDtoolbox/Mshdist.git"

    maintainers("jcortial-safran")

    version("master", branch="master")
    version(
        "1.0.0",
        sha256="4225effe3c64bcdffd8f43a2d7306c7c9f46e6e9817310280602843a3c784ec2",
        preferred=True,
    )

    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("iscdtoolbox-commons +openmp", when="+openmp")
    depends_on("iscdtoolbox-commons ~openmp", when="~openmp")

    patch("user-defined-prefix-path.patch")
