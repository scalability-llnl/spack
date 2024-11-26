# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOptree(PythonPackage):
    """Optimized PyTree Utilities."""

    homepage = "https://github.com/metaopt/optree"
    pypi = "optree/optree-0.10.0.tar.gz"

    license("Apache-2.0")

    version("0.10.0", sha256="dc7e8880f997365083191784d141c790833877af71aec8825c7f2b7f7f43c98e")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.11:", type="build")
    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", type=("build", "link"))
    depends_on("py-typing-extensions@4:", type=("build", "run"))
