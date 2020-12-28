# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gccmakedep(AutotoolsPackage, XorgPackage):
    """X.org gccmakedep utilities."""

    homepage = "https://cgit.freedesktop.org/xorg/util/gccmakedep/"
    xorg_mirror_path = "util/gccmakedep-1.0.3.tar.gz"

    version('1.0.3', sha256='f9e2e7a590e27f84b6708ab7a81e546399b949bf652fb9b95193e0e543e6a548')

    depends_on('pkgconfig', type='build')
