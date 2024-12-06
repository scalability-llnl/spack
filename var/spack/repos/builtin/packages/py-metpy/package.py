# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetpy(PythonPackage):
    """Collection of tools for reading, visualizing and performing calculations
    with weather data."""

    homepage = "https://github.com/Unidata/MetPy"
    pypi = "MetPy/MetPy-1.0.1.tar.gz"
    maintainers("dopplershift")

    # Importing 'metpy.io' results in downloads, so skip it.
    # https://github.com/Unidata/MetPy/issues/1888
    import_modules = ["metpy", "metpy._vendor", "metpy.calc", "metpy.interpolate"]

    license("BSD-3-Clause")

    version("1.6.2", sha256="eb065bac0d7818587fa38fa6c96dfe720d9d15b59af4e4866541894e267476bb")
    version("1.0.1", sha256="16fa9806facc24f31f454b898741ec5639a72ba9d4ff8a19ad0e94629d93cb95")

    variant(
        "extras",
        default=False,
        when="@1.6.2:",
        description="Enable xarray lazy-loading and advanced plotting",
    )

    with when("@1.6.2"):
        depends_on("python@3.9:", type=("build", "run"))
        depends_on("py-setuptools@61:", type="build")
        depends_on("py-setuptools-scm@3.4:", type="build")
        depends_on("py-matplotlib@3.5.0:", type=("build", "run"))
        depends_on("py-numpy@1.20.0:", type=("build", "run"))
        depends_on("py-pandas@1.4.0:", type=("build", "run"))
        depends_on("py-pint@0.17:", type=("build", "run"))
        depends_on("py-pooch@1.2.0:", type=("build", "run"))
        depends_on("py-pyproj@3.0.0:", type=("build", "run"))
        depends_on("py-scipy@1.8.0:", type=("build", "run"))
        depends_on("py-traitlets@5.0.5:", type=("build", "run"))
        depends_on("py-xarray@0.21.0:", type=("build", "run"))

        depends_on("py-cartopy@0.12.0:", when="+extras")
        depends_on("py-dask@2020.12.0:", when="+extras")
        depends_on("py-shapely@1.6.4:", when="+extras")

    with when("@1.0.1"):
        depends_on("python@3.6:", type=("build", "run"))
        depends_on("py-setuptools", type="build")
        depends_on("py-setuptools-scm", type="build")
        depends_on("py-importlib-metadata@1.0.0:", when="^python@:3.7", type=("build", "run"))
        depends_on("py-importlib-resources@1.3.0:", when="^python@:3.8", type=("build", "run"))
        depends_on("py-matplotlib@2.1.0:", type=("build", "run"))
        depends_on("py-numpy@1.16.0:", type=("build", "run"))
        depends_on("py-pandas@0.24.0:", type=("build", "run"))
        # Unable to Find "pint.unit" -- Module Not Found Error with py-pint@0.20:
        depends_on("py-pint@0.10.1:0.19", type=("build", "run"))
        depends_on("py-pooch@0.1:", type=("build", "run"))
        depends_on("py-pyproj@2.3.0:", type=("build", "run"))
        depends_on("py-scipy@1.0:", type=("build", "run"))
        depends_on("py-traitlets@4.3.0:", type=("build", "run"))
        depends_on("py-xarray@0.14.1:", type=("build", "run"))
