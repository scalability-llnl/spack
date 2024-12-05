# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsolv(CMakePackage):
    """Library for solving packages and reading repositories."""

    homepage = "https://en.opensuse.org/OpenSUSE:Libzypp_satsolver"
    url = "https://github.com/opensuse/libsolv/archive/0.7.22.tar.gz"

    maintainers("charmoniumQ")

    license("BSD-3-Clause")

    version("0.7.22", sha256="968aef452b5493751fa0168cd58745a77c755e202a43fe8d549d791eb16034d5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("conda", default=False, description="Include solv/conda.h")

    depends_on("expat", type="link")
    depends_on("zlib-api", type="link")

    def cmake_args(self):
        return [
            self.define("ENABLE_STATIC", self.spec.satisfies("~shared")),
            self.define("DISABLE_DYNAMIC", self.spec.satisfies("~shared")),
            self.define_from_variant("ENABLE_CONDA", "conda"),
        ]
