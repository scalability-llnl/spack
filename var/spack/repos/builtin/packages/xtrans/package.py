# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtrans(AutotoolsPackage, XorgPackage):
    """xtrans is a library of code that is shared among various X packages to
    handle network protocol transport in a modular fashion, allowing a
    single place to add new transport types.  It is used by the X server,
    libX11, libICE, the X font server, and related components."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libxtrans"
    xorg_mirror_path = "lib/xtrans-1.3.5.tar.gz"

    version('1.3.5', sha256='b7a577c1b6c75030145e53b4793db9c88f9359ac49e7d771d4385d21b3e5945d')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
