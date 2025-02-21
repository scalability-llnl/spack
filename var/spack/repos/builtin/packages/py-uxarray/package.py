# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUxarray(PythonPackage):
    """Xarray extension for unstructured climate and global weather data analysis and
    visualization"""

    homepage = "https://uxarray.readthedocs.io"
    pypi = "uxarray/uxarray-2024.10.0.tar.gz"
    git = "https://github.com/uxarray/uxarray.git"

    license("Apache-2.0", checked_by="climbfuji")

    version("2024.10.0", sha256="f65a9920ce085af9a38349dc5ece4f9b83bc015dc8cb738d245d343f7816fd59")

    # Build-time dependencies
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@60:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")

    # "Minimal" run-time dependencies
    depends_on("py-antimeridian", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-datashader", type="run")
    depends_on("py-geopandas", type="run")
    depends_on("py-geoviews", type="run")
    depends_on("py-holoviews", type="run")
    depends_on("py-hvplot", type="run")
    # With older versions of py-dask (2021.6.2):
    #    @derived_from(pd.core.strings.StringMethods)
    #                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #    AttributeError: module 'pandas.core.strings' has no attribute 'StringMethods'
    # With py-dask@2023.4.1:
    #      return get(descriptor, obj, type(obj))
    #                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #      TypeError: descriptor '__call__' for 'type' objects doesn't apply to a 'property' object
    # https://github.com/dask/dask/issues/11038
    depends_on("py-dask@2024.7.1 +dataframe", type="run")
    depends_on("py-dask-expr@1.1.9", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-matplotlib-inline", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-numba", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pyarrow", type="run")
    depends_on("py-pytest", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-spatialpandas", type="run")
    depends_on("py-scikit-learn", type="run")
    depends_on("py-xarray", type="run")
