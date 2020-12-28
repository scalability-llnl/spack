# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfs(AutotoolsPackage, XorgPackage):
    """libFS - X Font Service client library.

    This library is used by clients of X Font Servers (xfs), such as
    xfsinfo, fslsfonts, and the X servers themselves."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libFS"
    xorg_mirror_path = "lib/libFS-1.0.7.tar.gz"

    version('1.0.7', sha256='91bf1c5ce4115b7dbf4e314fdbee54052708e8f7b6a2ec6e82c309bcbe40ef3d')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('fontsproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
