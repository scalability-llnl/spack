# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHpack(PythonPackage):
    """Pure-Python HPACK header compression"""

    homepage = "https://github.com/python-hyper/hpack"
    pypi = "hpack/hpack-4.0.0.tar.gz"

    license("MIT")

    version("4.0.0", sha256="fc41de0c63e687ebffde81187a948221294896f6bdc0ae2312708df339430095")
    version("3.0.0", sha256="8eec9c1f4bfae3408a3f30500261f7e6a65912dc138526ea054f9ad98892e9d2")

    depends_on("python@3.6.1:", type=("build", "run"), when="@4:")
    depends_on("py-setuptools", type="build")
