# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatacube(PythonPackage):
    """An analysis environment for satellite and other earth observation data."""

    homepage = "https://github.com/opendatacube/datacube-core"
    pypi = "datacube/datacube-1.8.3.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("1.8.3", sha256="d1e1a49c615fdaebf6e6008da7f925bc09e9d7bf94f259a1c596d266d1c36649")

    # Excluding 'datacube.utils.aws' since it requires 'boto3'
    import_modules = [
        "datacube_apps",
        "datacube_apps.stacker",
        "datacube",
        "datacube.ui",
        "datacube.drivers",
        "datacube.drivers.rio",
        "datacube.drivers.postgres",
        "datacube.drivers.netcdf",
        "datacube.utils",
        "datacube.utils.rio",
        "datacube.utils.geometry",
        "datacube.storage",
        "datacube.execution",
        "datacube.virtual",
        "datacube.scripts",
        "datacube.model",
        "datacube.api",
        "datacube.index",
        "datacube.testutils",
    ]

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-affine", type=("build", "run"))
    depends_on("py-pyproj@2.5:", type=("build", "run"))
    depends_on("py-shapely@1.6.4:", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
    depends_on("py-click@5.0:", type=("build", "run"))
    depends_on("py-cloudpickle@0.4:", type=("build", "run"))
    depends_on("py-dask+array", type=("build", "run"))
    depends_on("py-distributed", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psycopg2", type=("build", "run"))
    depends_on("py-lark@0.6.7:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-rasterio@1.0.2:", type=("build", "run"))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-toolz", type=("build", "run"))
    depends_on("py-xarray@0.9:", type=("build", "run"))
