# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rclone(Package):
    """Rclone is a command line program to sync files and directories
       to and from various cloud storage providers"""

    homepage = "http://rclone.org"
    url      = "https://github.com/ncw/rclone/releases/download/v1.43/rclone-v1.43.tar.gz"

    version('1.51.0', sha256='3eb5b7ffce17e56fadb29bf854666723a14c93fedc02046c7f34c792dbd227ee')
    version('1.50.2', sha256='6dd8998a72514d3820d241ae46dc609c0305b742aee3db6aaf6017b46c996091')
    version('1.50.1', sha256='48d6c80883427469682b4d97099d7631cf3b67aa85e652c254423bd1422ce216')
    version('1.50.0', sha256='f901fd1752aae6116d94fd08d010a70d94535257c2d23caa505e631cce1e802a')
    version('1.49.5', sha256='abd2c83d71c63a4b0a30b1980b942868e707d05e14ae76ad39abf5cc5a5fde63')
    version('1.49.4', sha256='070afc85e4e9921151d7cb67247db8f0ff2f06fcf2652c43a42fa6e1e35847af')
    version('1.43', sha256='d30527b00cecb4e5e7188dddb78e5cec62d67cf2422dab82190db58512b5a4e3')

    depends_on("go", type='build')

    def setup_build_environment(self, env):
        # Point GOPATH at the top of the staging dir for the build step.
        env.prepend_path('GOPATH', self.stage.path)

    def install(self, spec, prefix):
        go('build')
        mkdirp(prefix.bin)
        install('rclone', prefix.bin)
