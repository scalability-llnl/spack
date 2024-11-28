# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5netcdf(PythonPackage):
    """A Python interface for the netCDF4 file-format that reads and writes local or
    remote HDF5 files directly via h5py or h5pyd, without relying on the Unidata netCDF
    library."""

    homepage = "https://github.com/h5netcdf/h5netcdf"
    pypi = "h5netcdf/h5netcdf-0.10.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.0", sha256="a171c027daeb34b24c24a3b6304195b8eabbb6f10c748256ed3cfe19806383cf")
    version("0.10.0", sha256="fc1cfec33bb9f730c412f87fcbc259167fd7620635679ccfc6e31971730dbd60")

    depends_on("python@3.9:", when="@1.3:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@1.3:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@7:+toml", when="@1.3:", type="build")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-packaging", when="@1.3:", type=("build", "run"))
