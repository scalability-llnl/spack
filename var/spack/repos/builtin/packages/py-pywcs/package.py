# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPywcs(PythonPackage):
    """pywcs is a set of routines for
    handling the FITS World Coordinate System (WCS) standard."""

    homepage = "https://github.com/spacetelescope/pywcs"
    url      = "https://github.com/spacetelescope/pywcs/archive/1.12.1.tar.gz"

    version('1.12.1', sha256='efd4e0ea190e3a2521ebcde583452e126acdeac85cc8a9c78c8a96f10805b5e1')

    depends_on('py-d2to1', type='build')
    depends_on('py-stsci-distutils', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyfits', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
