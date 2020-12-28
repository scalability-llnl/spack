# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FuseOverlayfs(AutotoolsPackage):
    """An implementation of overlay+shiftfs in FUSE for rootless containers."""

    homepage = "https://github.com/containers/fuse-overlayfs"
    url      = "https://github.com/containers/fuse-overlayfs/archive/v1.1.2.tar.gz"

    version('1.1.2', sha256='1c0fa67f806c44d5c51f4bce02fdcb546137a2688a8de76d93d07b79defc9cac')
    version('1.1.1', sha256='9a1c4221a82059fd9686dd8b519d432bae126c08f9d891fb722bcb51ba4933ec')
    version('1.1.0', sha256='060168c2d5a8c6cc768b4542eba9953b7ff4a31f94bfb2e05b3d1051390838b1')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libfuse')
