# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Glew(CMakePackage):
    """The OpenGL Extension Wrangler Library."""

    homepage = "http://glew.sourceforge.net/"
    url      = "https://github.com/nigels-com/glew/releases/download/glew-2.1.0/glew-2.1.0.tgz"

    version('2.1.0',  sha256='04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95')
    version('2.0.0',  sha256='c572c30a4e64689c342ba1624130ac98936d7af90c3103f9ce12b8a0c5736764')

    depends_on("gl")
    depends_on('libsm')
    depends_on('libice')

    root_cmakelists_dir = "build/cmake"

    @run_after('cmake')
    def patch_glew_pc(self):
        # https://github.com/Homebrew/legacy-homebrew/issues/22025
        # Note: This file is generated only after cmake is run
        filter_file(r'Requires: glu', '', 'glew.pc')
