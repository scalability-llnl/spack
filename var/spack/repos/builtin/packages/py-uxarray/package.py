# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUxarray(PythonPackage):
    """Xarray extension for unstructured climate and global weather data analysis and visualization"""

    homepage = "https://uxarray.readthedocs.io"
    pypi = "uxarray/uxarray-2024.10.0.tar.gz"
    #pypi = "uxarray/uxarray-2023.11.1.tar.gz"
    git = "https://github.com/uxarray/uxarray.git"


    ## 'xarray.tests' requires 'pytest'. Leave out of 'import_modules' to avoid
    ## unnecessary dependency.
    #import_modules = [
    #    "xarray",
    #    "xarray.core",
    #    "xarray.plot",
    #    "xarray.util",
    #    "xarray.backends",
    #    "xarray.coding",
    #]

    license("Apache-2.0", checked_by="climbfuji")

    version("2024.10.0", sha256="f65a9920ce085af9a38349dc5ece4f9b83bc015dc8cb738d245d343f7816fd59")
    #version("2023.11.1", sha256="fc580b5b6200594bf89d61cd345a275cfef43035e5b038d7e4e83d0d95062838")

    # pyproject.toml
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@60:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")

    # "Minimal" dependencies for 2024 version
    ### depends_on("py-antimeridian", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-datashader", type="run")
    depends_on("py-geopandas", type="run")
    depends_on("py-geoviews", type="run")
    depends_on("py-holoviews", type="run")
    #depends_on("py-hvplot", type="run")
    depends_on("py-dask +dataframe", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-matplotlib-inline", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-numba", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pyarrow", type="run")
    depends_on("py-pytest", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-scipy", type="run")
    #depends_on("py-spatialpandas", type="run")
    depends_on("py-scikit-learn", type="run")
    depends_on("py-xarray", type="run")

    # For versions 2024.*.*, from pyproject.toml:
    ## minimal dependencies start
    #dependencies = [
    # OK #  "antimeridian",
    # OK #  "cartopy",
    # OK #  "dask[dataframe]",
    # OK # "datashader",
    # OK #  "geoviews",
    # OK #  "holoviews",
    # OK #  "matplotlib",
    # OK #  "matplotlib-inline",
    # OK #  "netcdf4",
    # OK #  "numba",
    # OK #  "numpy",
    # OK #  "pandas",
    # OK #  "pyarrow",
    # OK #  "requests",
    # OK #  "scikit-learn",
    # OK #  "scipy",
    # OK #  "shapely",
    # OK #  "spatialpandas",
    # OK #  "geopandas",
    # OK #  "xarray",
    # OK #  "hvplot",
    #]
