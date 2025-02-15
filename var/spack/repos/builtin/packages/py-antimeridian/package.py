# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAntimeridian(PythonPackage):
    """Fix shapes that cross the antimeridian."""

    homepage = "https://antimeridian.readthedocs.io/"
    pypi = "antimeridian/antimeridian-0.3.11.tar.gz"
    git = "https://github.com/gadomski/antimeridian.git"

    license("Apache-2.0")

    version("0.3.11", sha256="fde0134e6799676ec68765d3e588f5f32cabd4041b1f969b923758d0a6cd0c7f")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-hatchling", type="build")

    depends_on("py-numpy@1.22.4:", type="run")
    depends_on("py-shapely@2:", type="run")
