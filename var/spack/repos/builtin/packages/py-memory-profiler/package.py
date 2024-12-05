# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMemoryProfiler(PythonPackage):
    """A module for monitoring memory usage of a python program"""

    homepage = "https://github.com/pythonprofilers/memory_profiler"
    pypi = "memory_profiler/memory_profiler-0.57.0.tar.gz"

    version("0.61.0", sha256="4e5b73d7864a1d1292fb76a03e82a3e78ef934d06828a698d9dada76da2067b0")
    version("0.60.0", sha256="6a12869511d6cebcb29b71ba26985675a58e16e06b3c523b49f67c5497a33d1c")
    version("0.57.0", sha256="23b196f91ea9ac9996e30bfab1e82fecc30a4a1d24870e81d1e81625f786a2c3")
    version("0.47", sha256="e992f2a341a5332dad1ad4a008eeac7cfe78c7ea4abdf7535a3e7e79093328cb")

    depends_on("python@3.5:", when="@0.61:", type=("build", "run"))
    depends_on("python@3.4:", when="@0.59:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-psutil", type=("build", "run"))
