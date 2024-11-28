# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bueno(PythonPackage):
    """Bueno: Well-Provenanced Benchmarking"""

    homepage = "https://lanl.github.io/bueno"
    url = "https://github.com/lanl/bueno/archive/refs/tags/v0.0.1.tar.gz"
    git = "https://github.com/lanl/bueno.git"

    maintainers("rbberger")

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-lark@1.0.0", type=("build", "run"))
    depends_on("py-pika@1.2.0", type=("build", "run"))

    depends_on("py-setuptools", type="build")
