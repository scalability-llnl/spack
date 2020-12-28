# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCrcmod(PythonPackage):
    """Python module for generating objects that
       compute the Cyclic Redundancy Check (CRC)"""

    homepage = "http://crcmod.sourceforge.net/"
    url      = "https://pypi.io/packages/source/c/crcmod/crcmod-1.7.tar.gz"

    version('1.7', sha256='dc7051a0db5f2bd48665a990d3ec1cc305a466a77358ca4492826f41f283601e')
    version('1.6', sha256='56d27d035ea029c6ed96779ca042c0136d39d106e3c30baa6422738c7d86aaa5')

    depends_on('python@2.4:2.7,3.1:', type=('build', 'run'))
    depends_on('py-setuptools@40.0.0:', type='build')

    def install(self, spec, prefix):
        # Override install to avoid
        #   error: option --single-version-externally-managed not recognized
        setup_py('install', '--root=/', '--prefix={0}'.format(prefix))
