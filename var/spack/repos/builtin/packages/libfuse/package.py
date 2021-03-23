# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfuse(MesonPackage):
    """The reference implementation of the Linux FUSE (Filesystem in
    Userspace) interface"""

    homepage = "https://github.com/libfuse/libfuse"
    url      = "https://github.com/libfuse/libfuse/archive/fuse-3.9.3.tar.gz"

    version('3.10.2', sha256='a16f93cc083264afd0d2958a0dc88f24c6c5d40a9f3842c645b1909e13edb75f')
    version('3.10.1', sha256='d8954e7b4c022c651aa80db3bb4a161437dd285cd5f1a23d0e25f055dcebe00d')
    version('3.10.0', sha256='52bbb52035f7eeaa54d139e21805d357f848f6e02ac956831d04988165a92c7b')
    version('3.9.4',  sha256='9e076ae757a09cac9ce1beb50b3361ae83a831e5abc0f1bf5cdf771cd1320338')
    version('3.9.3',  sha256='0f8f7ad9cc6667c6751efa425dd0a665dcc9d75f0b7fc0cb5b85141a514110e9')
    version('3.9.2',  sha256='b4409255cbda6f6975ca330f5b04cb335b823a95ddd8c812c3d224ec53478fc0')

    variant('useroot', default=False)

    def meson_args(self):
        args = []

        if '+useroot' in self.spec:
            args.append('-Duseroot=true')
        else:
            args.append('-Duseroot=false')

        return args
