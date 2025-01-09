# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCftime(PythonPackage):
    """Python library for decoding time units and variable values in a
    netCDF file conforming to the Climate and Forecasting (CF)
    netCDF conventions"""

    homepage = "https://unidata.github.io/cftime/"
    url = "https://github.com/Unidata/cftime/archive/refs/tags/v1.0.3.4rel.tar.gz"

    version("1.0.3.4", sha256="f261ff8c65ceef4799784cd999b256d608c177d4c90b083553aceec3b6c23fd3")

    depends_on("py-setuptools@18.0:", type="build")
    depends_on("py-cython@0.19:", type="build")
    depends_on("py-numpy", type=("build", "run"))
