# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonFmask(PythonPackage):
    """A set of command line utilities and Python modules that implement
       the FMASK algorithm for Landsat and Sentinel-2"""

    homepage = "http://pythonfmask.org"
    url      = "https://github.com/ubarsc/python-fmask/archive/pythonfmask-0.5.4.tar.gz"

    version('0.5.4', sha256='a216aa3108de837fec182602b2b4708442746be31fc1585906802437784a63fe')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-rios',       type=('build', 'run'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('gdal+python',   type=('build', 'run'))
