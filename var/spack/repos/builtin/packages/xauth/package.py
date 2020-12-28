# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xauth(AutotoolsPackage, XorgPackage):
    """The xauth program is used to edit and display the authorization
    information used in connecting to the X server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xauth"
    xorg_mirror_path = "app/xauth-1.0.9.tar.gz"

    version('1.0.9', sha256='0709070caf23ba2fb99536907b75be1fe31853999c62d3e87a6a8d26ba8a8cdb')

    depends_on('libx11')
    depends_on('libxau')
    depends_on('libxext')
    depends_on('libxmu')

    depends_on('xproto@7.0.17:')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    # TODO: add package for cmdtest test dependency
