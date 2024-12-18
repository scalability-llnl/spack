# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNodeenv(PythonPackage):
    """Node.js virtual environment"""

    homepage = "https://github.com/ekalinin/nodeenv"
    pypi = "nodeenv/nodeenv-1.3.3.tar.gz"

    version("1.9.1", sha256="6ec12890a2dab7946721edbfbcd91f3319c6ccc9aec47be7c7e6b7011ee6645f")
    version("1.8.0", sha256="d51e0c37e64fbf47d017feac3145cdbb58836d7eee8c6f6d3b6880c5456227d2")
    version("1.7.0", sha256="e0e7f7dfb85fc5394c6fe1e8fa98131a2473e04311a45afb6508f7cf1836fa2b")
    version("1.3.3", sha256="ad8259494cf1c9034539f6cced78a1da4840a4b157e23640bc4a0c0546b0cb7a")

    with default_args(type=("build", "run")):
        # https://github.com/ekalinin/nodeenv/commit/c1dffc5c64377cfcda9f2befd357e4791903bf39
        depends_on("python@:3.12", when="@:1.8")
        depends_on("python +ssl", when="@1.5:")
        depends_on("py-setuptools", when="@1.7:")

    depends_on("py-setuptools", type="build")
