# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyElevation(PythonPackage):
    """
    Python script to download global terrain digital elevation models,
    SRTM 30m DEM and SRTM 90m DEM.
    """

    homepage = "http://elevation.bopen.eu/"
    pypi = "elevation/elevation-1.1.3.tar.gz"

    maintainers("Chrismarsh")

    license("Apache-2.0", checked_by="Chrismarsh")

    version("1.1.3", sha256="be27446562e7964f7d8fa78c4829dbbb8ac43df405ad09be8c49633adb8f4877")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-click", type="build")

    depends_on("py-fasteners")
    depends_on("py-rasterio")
    depends_on("py-fiona")
    depends_on("py-appdirs")

    # listed in
    # https://github.com/bopen/elevation/blob/1.1.3/README.rst
    depends_on("curl")
    depends_on("unzip")
    depends_on("gzip")
    depends_on("gdal+python")
