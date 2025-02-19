# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlox(PythonPackage):
    """Fast & furious GroupBy operations for dask.array."""

    homepage = "https://github.com/xarray-contrib/flox"
    pypi = "flox/flox-0.10.0.tar.gz"

    maintainers("Chrismarsh")

    license("Apache-2.0", checked_by="Chrismarsh")

    version("0.10.0", sha256="4d326f13597c99ea0ce260b54f4c88d071445816efc83e42e3f8d4030e835654")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-setuptools-scm@7.0: +toml", type="build")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-pandas@1.5:", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"))
    depends_on("py-numpy@1.22:", type=("build", "run"))
    depends_on("py-numpy-groupies@0.9.19:", type=("build", "run"))
    depends_on("py-toolz", type=("build", "run"))
    depends_on("py-scipy@1.9:", type=("build", "run"))
