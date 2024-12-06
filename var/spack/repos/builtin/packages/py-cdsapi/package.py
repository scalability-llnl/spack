# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCdsapi(PythonPackage):
    """Climate Data Store API."""

    homepage = "https://cds.climate.copernicus.eu"
    pypi = "cdsapi/cdsapi-0.2.3.tar.gz"

    license("Apache-2.0")

    version("0.6.1", sha256="7d40c58e3fd3e75a8acdcdc81eab4ef9b6f763b2902ba01d7d1738f3652a5a30")
    version("0.2.3", sha256="333b31ec263224399635db9b21a2e1a50cd73451f5179f8d967437e7c9161d9b")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.5.0:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
