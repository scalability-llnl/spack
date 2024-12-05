# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibconf(PythonPackage):
    """A pure-Python libconfig reader/writer with permissive license"""

    pypi = "libconf/libconf-2.0.1.tar.gz"

    license("MIT")

    version("2.0.1", sha256="2f907258953ba60a95a82d5633726b47c81f2d5cf8d8801b092579016d757f4a")
    version("1.0.1", sha256="6dd62847bb69ab5a09155cb8be2328cce01e7ef88a35e7c37bea2b1a70f8bd58")

    depends_on("py-setuptools", type="build")
