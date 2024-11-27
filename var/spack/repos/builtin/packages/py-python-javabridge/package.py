# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonJavabridge(PythonPackage):
    """The python-javabridge package makes it easy to start a
    Java virtual machine (JVM) from Python and interact with it."""

    homepage = "https://github.com/CellProfiler/python-javabridge/"
    pypi = "python-javabridge/python-javabridge-4.0.3.tar.gz"

    version("4.0.3", sha256="3fee0c235efcfe866f95695fdc0b6289eab2371043b32ff4ca6feff098de59c5")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.16:", type="build")
    depends_on("py-numpy@1.20.1:", type=("build", "run"))
    depends_on("java", type=("build", "run", "link"))
