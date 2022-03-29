# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Neko(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Neko: A modern, portable, and scalable framework
       for high-fidelity computational fluid dynamics
    """

    homepage = "https://github.com/ExtremeFLOW/neko"
    git      = "https://github.com/ExtremeFLOW/neko.git"
    maintainers = ['njansson']

    version('0.3.0', tag='v0.3.0')
    version('develop', branch='develop')
    variant('parmetis', default=False, description='Build with support for parmetis')
    variant('xsmm', default=False, description='Build with support for libxsmm')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('pkgconf',  type='build')
    depends_on('parmetis', when='+parmetis')
    depends_on('libxsmm',  when='+xsmm')
    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        args = []
        if '+parmetis' in self.spec:
            args.append('--with-parmetis')
        if '+xsmm' in self.spec:
            args.append('--with-libxsmm')
        if '+cuda' in self.spec:
            args.append('--with-cuda={0}'.format(self.spec['cuda'].prefix))
        if '+rocm' in self.spec:
            args.append('--with-hip={0}'.format(self.spec['hip'].prefix))

        return args
