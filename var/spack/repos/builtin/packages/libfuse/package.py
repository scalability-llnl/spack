# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfuse(MesonPackage):
    """The reference implementation of the Linux FUSE (Filesystem in
    Userspace) interface"""

    homepage = "https://github.com/libfuse/libfuse"
    url      = "https://github.com/libfuse/libfuse/archive/fuse-3.9.3.tar.gz"

    version('3.9.4', sha256='9e076ae757a09cac9ce1beb50b3361ae83a831e5abc0f1bf5cdf771cd1320338')
    version('3.9.3', sha256='0f8f7ad9cc6667c6751efa425dd0a665dcc9d75f0b7fc0cb5b85141a514110e9')
    version('3.9.2', sha256='b4409255cbda6f6975ca330f5b04cb335b823a95ddd8c812c3d224ec53478fc0')
