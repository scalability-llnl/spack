# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lsd(CargoPackage):
    """A rewrite of GNU ls with lots of added features like colors, icons, tree-view,
    more formatting options etc."""

    homepage = "https://github.com/lsd-rs/lsd"
    url = "https://github.com/lsd-rs/lsd/archive/refs/tags/v1.0.0.tar.gz"

    maintainers("trws")

    license("Apache-2.0")

    version("1.0.0", sha256="ab34e9c85bc77cfa42b43bfb54414200433a37419f3b1947d0e8cfbb4b7a6325")

    depends_on("rust@1.63:")
