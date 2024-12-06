# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestBenchmark(PythonPackage):
    """A pytest fixture for benchmarking code."""

    homepage = "https://github.com/ionelmc/pytest-benchmark"
    pypi = "pytest-benchmark/pytest-benchmark-3.2.3.tar.gz"

    license("BSD-2-Clause")

    version("3.2.3", sha256="ad4314d093a3089701b24c80a05121994c7765ce373478c8f4ba8d23c9ba9528")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@3.8:", type=("build", "run"))
    depends_on("py-py-cpuinfo", type=("build", "run"))
