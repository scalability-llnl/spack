# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRefgenconf(PythonPackage):
    """A Python object for standardized reference genome assets."""

    homepage = "https://github.com/refgenie/refgenconf"
    pypi = "refgenconf/refgenconf-0.12.2.tar.gz"

    license("BSD-2-Clause")

    version("0.12.2", sha256="6c9f9ecd8b91b4f75a535cfbdbdfb136f2dc9e9864142d07aa0352c61cf0cf78")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-future", type=("build", "run"))
    depends_on("py-jsonschema@3.0.1:", type=("build", "run"))
    depends_on("py-pyfaidx", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-rich@9.0.1:", type=("build", "run"))
    depends_on("py-yacman@0.8.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
