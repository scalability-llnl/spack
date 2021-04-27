# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glm(CMakePackage):
    """OpenGL Mathematics (GLM) is a header only C++ mathematics library for
    graphics software based on the OpenGL Shading Language (GLSL) specification
    """

    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/g-truc/glm/archive/0.9.9.8.tar.gz"

    version('0.9.9.8', sha256='7d508ab72cb5d43227a3711420f06ff99b0a0cb63ee2f93631b162bfe1fe9592')
    version('0.9.7.1', sha256='285a0dc8f762b4e523c8710fbd97accaace0c61f45bc8be2bdb0deed07b0e6f3')

    depends_on('cmake@2.6:', type='build')
    depends_on('cmake@3.2:', type='build', when='@0.9.9.0:')

    # CMake install target was removed in version 0.9.9.6
    @when('@0.9.9.6:')
    def cmake(self, spec, prefix):
        pass

    @when('@0.9.9.6:')
    def build(self, spec, prefix):
        pass

    @when('@0.9.9.6:')
    def install(self, spec, prefix):
        mkdirp(prefix.include.glm)
        ignore_cmakelists = lambda p: p.endswith('CMakeLists.txt')
        install_tree('glm', prefix.include.glm, ignore=ignore_cmakelists)
        mkdirp(prefix.lib64.cmake)
        install_tree('cmake', prefix.lib64.cmake)
