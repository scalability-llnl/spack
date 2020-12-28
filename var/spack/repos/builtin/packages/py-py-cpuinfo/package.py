# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyCpuinfo(PythonPackage):
    """Get CPU info with pure Python 2 & 3"""

    homepage = "https://github.com/workhorsy/py-cpuinfo"
    url      = "https://pypi.io/packages/source/p/py-cpuinfo/py-cpuinfo-0.2.3.tar.gz"

    version('0.2.3', sha256='f6a016fdbc4e7fadf2d519090fcb4fa9d0831bad4e85245d938e5c2fe7623ca6')

    depends_on('py-setuptools', type='build')
