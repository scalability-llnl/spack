# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyH5netcdf(PythonPackage):
    """A Python interface for the netCDF4 file-format that reads and writes local or
    remote HDF5 files directly via h5py or h5pyd, without relying on the Unidata netCDF
    library."""

    homepage = "https://github.com/h5netcdf/h5netcdf"
    pypi     = "h5netcdf/h5netcdf-0.10.0.tar.gz"

    version('0.10.0', sha256='fc1cfec33bb9f730c412f87fcbc259167fd7620635679ccfc6e31971730dbd60')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-h5py', type=('build', 'run'))
