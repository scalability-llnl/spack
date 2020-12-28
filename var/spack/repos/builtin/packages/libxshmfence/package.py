# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxshmfence(AutotoolsPackage, XorgPackage):
    """libxshmfence - Shared memory 'SyncFence' synchronization primitive.

    This library offers a CPU-based synchronization primitive compatible
    with the X SyncFence objects that can be shared between processes
    using file descriptor passing."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libxshmfence/"
    xorg_mirror_path = "lib/libxshmfence-1.3.tar.bz2"

    version('1.3', sha256='b884300d26a14961a076fbebc762a39831cb75f92bed5ccf9836345b459220c7')
    version('1.2', sha256='d21b2d1fd78c1efbe1f2c16dae1cb23f8fd231dcf891465b8debe636a9054b0c')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
