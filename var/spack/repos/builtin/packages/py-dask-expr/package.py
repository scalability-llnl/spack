# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskExpr(PythonPackage):
    """Dask DataFrames with query optimization."""

    homepage = "https://github.com/dask/dask-expr"
    url = "https://github.com/dask/dask-expr/archive/refs/tags/v1.1.9.tar.gz"

    license("BSD-3-Clause")

    version("1.1.9", sha256="e5a1b82de1142c29fed899a80541a98ca5e12cb85ce9d86bc8ada204a22599d3")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools@62.6:", type="build")
    depends_on("py-versioneer@0.28+toml", type="build")

    # Can't do circular run-time dependencies yet?
    # depends_on("py-dask@2024.7.1", type="run")
    depends_on("py-pyarrow@7: +dataset", type="run")
    depends_on("py-pandas@2:", type="run")
