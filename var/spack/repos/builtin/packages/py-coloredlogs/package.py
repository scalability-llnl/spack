# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColoredlogs(PythonPackage):
    """Colored terminal output for Python's logging module"""

    homepage = "https://pypi.org/project/coloredlogs/"
    url      = "https://pypi.io/packages/source/c/coloredlogs/coloredlogs-10.0.tar.gz"

    version('14.0', sha256='a1fab193d2053aa6c0a97608c4342d031f1f93a3d1218432c59322441d31a505')
    version('10.0', sha256='b869a2dda3fa88154b9dd850e27828d8755bfab5a838a1c97fbc850c6e377c36')

    depends_on('py-setuptools', type='build')
    depends_on('py-humanfriendly@4.7:', type=('build', 'run'))
