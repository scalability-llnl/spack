# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Openvslam(CMakePackage):
    """OpenVSLAM is a monocular, stereo, and RGBD visual SLAM system."""

    homepage = "https://openvslam.readthedocs.io/"
    git      = "https://github.com/xdspacelab/openvslam.git"

    version('master', branch='master')

    # https://openvslam.readthedocs.io/en/master/installation.html
    depends_on('cmake@3.1:', type='build')
    depends_on('eigen@3.3.0:')
    depends_on('g2o')
    depends_on('dbow2@shinsumicco')
    depends_on('yaml-cpp@0.6.0:')
    depends_on('opencv@3.3.1:+core+imgcodecs+videoio+features2d+calib3d+highgui')
    depends_on('pangolin')

    patch('https://github.com/xdspacelab/openvslam/commit/eeb58880443700fd79688d9646fd633c42fa60eb.patch',
          sha256='131159b0042300614d039ceb3538defe4d302b59dc748b02287fc8ff895e6bbd')

    @run_after('install')
    def post_install(self):
        # https://github.com/xdspacelab/openvslam/issues/501
        mkdir(self.prefix.bin)
        with working_dir(self.build_directory):
            install('run_*', self.prefix.bin)
            install(join_path('lib*', 'libpangolin_viewer.*'), self.prefix.lib)
