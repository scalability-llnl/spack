# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLiacArff(PythonPackage):
    """The liac-arff module implements functions to read and
    write ARFF files in Python."""

    homepage = "https://github.com/renatopp/liac-arff"
    pypi = "liac-arff/liac-arff-2.5.0.tar.gz"

    license("MIT")

    version("2.5.0", sha256="3220d0af6487c5aa71b47579be7ad1d94f3849ff1e224af3bf05ad49a0b5c4da")

    depends_on("python@2.7:2.999,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
