# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Prmon(CMakePackage):
    """Standalone monitor for process resource consumption."""

    homepage = "https://github.com/HSF/prmon/"
    url      = "https://github.com/HSF/prmon/archive/refs/tags/v2.2.0.zip"
    git      = "https://github.com/HSF/prmon.git"

    maintainers = ['vvolkl']

    version("master", branch="master")
    version('2.2.0', sha256='7b3b887c679279f0e666e8c8c58ca1a22a328b8b94ecff09e61795a6a83e8ce5')
    version('2.1.1', sha256='302d7a3fc5a403143d794e16dca1949e3d13e46cf9857dfaad4e374f4a468df2')
    version('1.1.1', sha256='a6e6486bbc4d6cddf73affe07d9ff7948a424c9a02b3cdd5bbe5c6cafa06af2e')

    variant('plot', default=True,
            description='Make use of plotting scripts')

    depends_on('nlohmann-json')
    depends_on('cmake@3.3:', type="build")
    depends_on('py-matplotlib', type="run", when="+plot")
