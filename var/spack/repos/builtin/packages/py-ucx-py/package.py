# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUcxPy(PythonPackage):
    """UCX-Py is the Python interface for UCX, a low-level
    high-performance networking library. UCX and UCX-Py supports
    several transport methods including InfiniBand and NVLink while
    still using traditional networking protocols like TCP."""

    homepage = "https://ucx-py.readthedocs.io/en/latest/"
    url = "https://github.com/rapidsai/ucx-py/archive/v0.16.0.tar.gz"

    license("Apache-2.0")

    version("0.16.0", sha256="12c1c982ee337b8dc026d3a6e8e63d96bf021c5c555fe173642908d3c3bec36e")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-cython@0.29.14:2", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pynvml", type=("build", "run"))
    depends_on("ucx")
    depends_on("hwloc")
