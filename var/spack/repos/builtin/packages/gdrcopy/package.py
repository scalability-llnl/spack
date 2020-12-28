# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gdrcopy(MakefilePackage):
    """A fast GPU memory copy library based on NVIDIA GPUDirect
       RDMA technology."""

    homepage = "https://github.com/NVIDIA/gdrcopy"
    url      = "https://github.com/NVIDIA/gdrcopy/archive/2.1.tar.gz"
    git      = "https://github.com/NVIDIA/gdrcopy"

    version('master', branch='master')
    version('2.1', sha256='cecc7dcc071107f77396f5553c9109790b6d2298ae29eb2dbbdd52b2a213e4ea')
    version('2.0', sha256='98320e6e980a7134ebc4eedd6cf23647104f2b3c557f2eaf0d31a02609f5f2b0')
    version('1.3', sha256='f11cdfe389b685f6636b80b4a3312dc014a385ad7220179c1318c60e2e28af3a')

    def url_for_version(self, version):
        if version >= Version('2.1'):
            return super(Gdrcopy, self).url_for_version(version)

        url_fmt = "https://github.com/NVIDIA/gdrcopy/archive/v{0}.tar.gz"
        return url_fmt.format(version)

    def build(self, spec, prefix):
        make('lib')

    def install(self, spec, prefix):
        mkdir(prefix.include)
        mkdir(prefix.lib64)
        make('lib_install', 'PREFIX={0}'.format(self.prefix))
