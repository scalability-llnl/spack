# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYtoptAutotune(PythonPackage):
    """Common interface for autotuning search space and method definition."""

    maintainers("Kerilk", "liuyangzhuan")

    homepage = "https://github.com/ytopt-team/autotune"
    url = "https://github.com/ytopt-team/autotune/archive/refs/tags/v1.1.0.tar.gz"
    git = "https://github.com/ytopt-team/autotune.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("1.1.0", sha256="5ee7fa6a1c83131c5ceba1537b25f00de84182e4d0e6ebd0fd6efa4e8aee1bc4")
    version("1.0.0", sha256="13f10594156a7a220561467fdbee52173238ea82c07e8188fdf6584d4524f46f")

    depends_on("c", type="build")  # generated

    patch("version.patch", when="@1.1.0")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
