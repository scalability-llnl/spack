# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IscdtoolboxAdvect(CMakePackage):
    """Advect is a program for solving linear advection problems in two and three dimensions."""

    homepage = "https://github.com/ISCDtoolbox"
    url = "https://github.com/ISCDtoolbox/Advection/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/ISCDtoolbox/Advection.git"

    maintainers("jcortial-safran")

    version("master", branch="master")
    version(
        "1.0.0",
        sha256="57d11c96a7a0662ee36b929504c97beee88daf5e978b8c091b106318103a0bb9",
        preferred=True,
    )

    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("iscdtoolbox-commons +openmp", when="+openmp")
    depends_on("iscdtoolbox-commons ~openmp", when="~openmp")

    patch("user-defined-prefix-path.patch")
