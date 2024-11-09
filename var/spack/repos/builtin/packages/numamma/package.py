# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Numamma(CMakePackage):
    """NumaMMa is a lightweight memory profiler that reports the
    memory access patterns of applications."""

    homepage = "https://numamma.github.io/numamma/"
    url = "https://github.com/numamma/numamma/archive/numamma-1.1.1.tar.gz"
    maintainers("trahay")

    license("MIT")

    version("1.1.1", sha256="f79ca22a95df33a1af529ddd653d043f7f0d32a6d196e559aee8bef8fc74771f")

    depends_on("c", type="build")  # generated

    depends_on("numap")
    depends_on("libbacktrace")
    depends_on("numactl")
    depends_on("libelf")

    def cmake_args(self):
        spec = self.spec
        cmake_args = ["-DBACKTRACE_DIR:PATH={0}".format(spec["libbacktrace"].prefix)]
        return cmake_args
