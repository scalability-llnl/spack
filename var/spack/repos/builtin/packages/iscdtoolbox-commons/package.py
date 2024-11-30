# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IscdtoolboxCommons(CMakePackage):
    """ISCDtoolbox -- Common definitions and functions (linear algebra, chrono, i/o...)"""

    homepage = "https://github.com/ISCDtoolbox"
    url = "https://github.com/ISCDtoolbox/Commons/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/ISCDtoolbox/Commons.git"

    maintainers("jcortial-safran")

    version("master", branch="master")
    version(
        "1.0.0",
        sha256="d230f8a786bf8f6a14db21243c71ccb9c5d408da5da89ae6f334d1339c10f83e",
        preferred=True,
    )

    variant("openmp", default=False, description="Enable OpenMP support")

    patch("user-defined-prefix-path.patch")

    def cmake_args(self):
        args = []
        if "+openmp" in self.spec:
            args.append(self.define_from_variant("OPENMP", "openmp"))
        return args
