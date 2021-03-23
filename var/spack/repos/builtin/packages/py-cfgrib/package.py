# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCfgrib(PythonPackage):
    """Python interface to map GRIB files to the NetCDF Common Data Model
    following the CF Convention using ecCodes."""

    homepage = "https://github.com/ecmwf/cfgrib"
    pypi     = "cfgrib/cfgrib-0.9.8.5.tar.gz"

    version('0.9.8.5', sha256='07c224d7ac823a1df5738b96b9d3621515538f51f67e55044f9cc8ec1668e1bd')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-attrs@19.2:', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
