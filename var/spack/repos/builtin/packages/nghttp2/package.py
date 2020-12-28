# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Nghttp2(AutotoolsPackage):
    """nghttp2 is an implementation of HTTP/2 and its header compression
       algorithm HPACK in C."""

    homepage = "https://nghttp2.org/"
    url      = "https://github.com/nghttp2/nghttp2/releases/download/v1.26.0/nghttp2-1.26.0.tar.gz"

    version('1.26.0', sha256='daf7c0ca363efa25b2cbb1e4bd925ac4287b664c3d1465f6a390359daa3f0cf1')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-cython@0.19:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))

    def setup_build_environment(self, env):
        site_packages_dir = os.path.join(
            self.spec.prefix.lib,
            'python' + str(self.spec['python'].version.up_to(2)),
            'site-packages')
        env.prepend_path('PYTHONPATH', site_packages_dir)

    @run_before('install')
    def ensure_install_dir_exists(self):
        site_packages_dir = os.path.join(
            self.spec.prefix.lib,
            'python' + str(self.spec['python'].version.up_to(2)),
            'site-packages')
        mkdirp(site_packages_dir)
