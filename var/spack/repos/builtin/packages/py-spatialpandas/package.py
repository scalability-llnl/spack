# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpatialpandas(PythonPackage):
    """Pandas extension arrays for spatial/geometric operations."""

    homepage = "https://holoviz.org/"
    pypi = "spatialpandas/spatialpandas-1.19.1.tar.gz"
    git = "https://github.com/holoviz/spatialpandas.git"

    license("BSD-2-Clause", checked_by="climbfuji")

    version("0.4.10", sha256="032e24ebb40f75c5c79cb79d7c281f2990e69ba382c0b24acb53da7bba60851c")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("py-param", type="build")

    depends_on("py-dask", type="run")
    depends_on("py-fsspec@2022.8:", type="run")
    depends_on("py-numba", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pyarrow@10:", type="run")
    depends_on("py-retrying", type="run")
