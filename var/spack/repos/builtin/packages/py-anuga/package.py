# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyAnuga(PythonPackage):
    """ANUGA (pronounced "AHnooGAH") is open-source software for the simulation
    of the shallow water equation, in particular it can be used to model
    tsunamis and floods."""

    homepage = "https://github.com/GeoscienceAustralia/anuga_core"
    url      = "https://github.com/GeoscienceAustralia/anuga_core/archive/2.1.tar.gz"

    version('2.1', sha256='0e56c4a7d55570d7b2c36fa9b53ee4e7b85f62be0b4c03ad8ab5f51464321d2f')

    variant('mpi', default=True, description='Install anuga_parallel')

    # At present AnuGA has only been run and tested using python 2.x.
    # We recommend python 2.7.
    depends_on('python@2.6:2.8', type=('build', 'run'))
    depends_on('py-setuptools@:44', type='build')
    depends_on('py-numpy@:1.16', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-matplotlib@:2', type=('build', 'run'))
    depends_on('gdal@:3.2+python', type=('build', 'run'))
    depends_on('py-pypar', when='+mpi', type=('build', 'run'))

    # https://github.com/GeoscienceAustralia/anuga_core/issues/247
    conflicts('%apple-clang@12:')
