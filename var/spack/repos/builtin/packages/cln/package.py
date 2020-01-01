# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cln(AutotoolsPackage):
    """CLN is a library for efficient computations with all kinds of numbers
    in arbitrary precision. It features number classes for unlimited length
    integers, rationals, arbitrary precision floating point numbers and much
    more."""

    homepage = "https://www.ginac.de/CLN/"
    git = "git://www.ginac.de/cln.git"

    version('1.3.4', commit='9b86a7fc69feb1b288469982001af565f73057eb')
    version('1.3.3', commit='1c9bd61ff0b89b0bf8030e44cb398e8f75112222')
    version('1.3.2', commit='00817f7b60a961b860f6d305ac82dd51b70d6ba6')
    version('1.3.1', commit='196fee3778494b69063f2a1b018e70de351b336f')
    version('1.3.0', commit='8e19c1a9d9ea4116112490d6f43904258b928649')
    version('1.2.2', commit='cd3ea9b9889856c6b54266fdb13b54dd3c53931a')
    version('1.2.1', commit='567378ab4cbfd443c3d82d810599860c769251fe')
    version('1.2.0', commit='679a0a8927f011fb32411f8a31070c77a9901094')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
