# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Prmon(CMakePackage):
    """Standalone monitor for process resource consumption."""

    homepage = "https://github.com/HSF/prmon/"
    url      = "https://github.com/HSF/prmon/archive/refs/tags/v3.0.1.zip"
    git      = "https://github.com/HSF/prmon.git"

    maintainers = ['graeme-a-stewart', 'amete', 'vvolkl']

    version("main", branch="main")
    version('3.0.1', sha256='c4eea2849e52e501d42f8e3f837e3f250691f7e7912b7503d6ca0a0e417ea474')
    version('3.0.0', sha256='bf6b27caa61d1fd9d1948b2a0595fa820ffbc58c1a423a7608f267392683f60f')
    version('2.2.1', sha256='d3ff37d5b3d246bd263cb538ad409d026a69742a029eea2f9fe1decebb3e7e78')
    version('2.2.0', sha256='7b3b887c679279f0e666e8c8c58ca1a22a328b8b94ecff09e61795a6a83e8ce5')
    version('2.1.1', sha256='302d7a3fc5a403143d794e16dca1949e3d13e46cf9857dfaad4e374f4a468df2')
    version('1.1.1', sha256='a6e6486bbc4d6cddf73affe07d9ff7948a424c9a02b3cdd5bbe5c6cafa06af2e')

    variant('plot', default=True,
            description='Make use of plotting scripts')

    depends_on('nlohmann-json')
    depends_on('cmake@3.3:', type="build")
    depends_on('py-matplotlib', type="run", when="+plot")
    depends_on('spdlog', when='@3.0.0:')
