# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFlattenDict(PythonPackage):
    """A flexible utility for flattening and unflattening dict-lik objects
    in Python"""

    homepage = "https://github.com/ianlini/flatten-dict"
    pypi = "flatten-dict/flatten-dict-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="0ccc43f15c7c84c5ef387ad19254f6769a32d170313a1bcbf4ce582089313d7e")

    depends_on("python@2.7,3.5:3", type=("build", "run"))
    depends_on("py-poetry@1:", type="build")
    depends_on("py-six@1.12:1", type=("build", "run"))
    depends_on("py-pathlib2@2.3:2", type=("build", "run"))
