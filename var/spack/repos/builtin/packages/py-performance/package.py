# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPerformance(PythonPackage):
    """The performance project is intended to be an authoritative source
    of benchmarks for all Python implementations.

    The focus is on real-world benchmarks, rather than synthetic benchmarks,
    using whole applications when possible.
    """

    homepage = "http://pyperformance.readthedocs.io/"
    url = "https://github.com/python/performance/archive/0.6.1.tar.gz"

    license("MIT")

    version("0.6.1", sha256="cc48dd7579da2f4b0e4cff0c8220811f5ba7019493bb408819c1532acf53d13a")
    version("0.6.0", sha256="4636e276445e96563f628e071cacd5df31dc587d83899e7d03fa8b31760f2cd2")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pyperf", type=("build", "run"))
