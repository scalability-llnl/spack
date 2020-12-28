# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xts(AutotoolsPackage, XorgPackage):
    """This is a revamped version of X Test Suite (XTS) which removes some of
    the ugliness of building and running the tests."""

    homepage = "https://www.x.org/wiki/XorgTesting/"
    xorg_mirror_path = "test/xts-0.99.1.tar.gz"

    version('0.99.1', sha256='d04d987b9a9f8b3921dfe8de8577d0c2a0f21d2c4c3196948fc9805838a352e6')

    depends_on('libx11', type='link')
    depends_on('libxext', type='link')
    depends_on('libxi', type='link')
    depends_on('libxtst', type='link')
    depends_on('libxau', type='link')
    depends_on('libxt', type='link')
    depends_on('libxmu', type='link')
    depends_on('libxaw', type='link')
    depends_on('inputproto', type='link')
    depends_on('recordproto', type='link')
    depends_on('fixesproto', type='link')

    depends_on('xtrans', type='build')
    depends_on('bdftopcf', type='build')
    depends_on('mkfontdir', type='build')
    depends_on('perl', type='build')
    depends_on('xset', type='build')
    depends_on('xdpyinfo', type='build')

    # FIXME: Crashes during compilation
    # error: redeclaration of enumerator 'XawChainTop'
